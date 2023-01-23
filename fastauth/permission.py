from typing import Dict, Optional, List
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from fastapi import Depends , HTTPException
from datetime import datetime
from .JWTBearer import JWTBearer
from .auth import jwks
from .db_connection import get_db
from sqlalchemy.orm import Session
from utils.check_exp import has_expired
auth = JWTBearer(jwks)

from fastauth.models import RolesEntities , Role


class CognitoJWTPermissionCheck:
    """
    This class will act as a dependency for every route
    with a given statment, the __call__ function will query
    in the roles_entities table to find all the roles related to the group
    then the method will check if the required statment is in one of those
    roles to grant permission for the user to use this route
    """
    def __init__(self , statements : List[str] ) -> None:

        # convert the statments list to a dictionary with
        # the list element as key and the values all False
        self.required_statements = self.list_to_dict(statements)
   
    def list_to_dict(self , list_of_strings):
        """
            This method converts a list of statements (strings) to a 
            dictionary where the statements are the keys and the value
            is False
        """
        new_dictionary = {}
        for item in list_of_strings:
            new_dictionary[item] = False
        return new_dictionary

    def get_role_statements(self, role_id : str , db : Session):
        role_record = db.query(Role).filter_by(id = role_id).one()
        try:
            return role_record.permissions["statements"]
        except KeyError:
            return []

    def find_group_roles(self , group_name : str , db : Session):

        group_roles = db.query(RolesEntities).filter_by(cognito_group_name = group_name)
        return list(group_roles)

    def validate_required_statements(self):
        
        """
            This method checks if all the values in the 
            self.required_statments dictionary are True
            if only in is False, The permission in denied
        """

        for k in list(self.required_statements.keys()):
            if not self.required_statements[k]:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail=f"Permission denied : User must have {k} permission"
                )

        return True

    def __call__(self , jwt_creds : dict = Depends(auth) , db : Session = Depends(get_db)):
        """
            This is the method get called at the Depend part of the route
            The __call__ method use as a dependency and relies on the fact 
            that any error that occurs throughout the checks will fail the 
            method and prevent the request to go over to the route in the API
        """
        
        # checks if the JWT has expired
        has_expired(expiration_date = dict(jwt_creds.claims)["exp"])

        # get the cognito groups from the JWT
        if not dict(jwt_creds.claims)["cognito:groups"]:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not related to any group"
            )
        else:
            cognito_groups = dict(jwt_creds.claims)["cognito:groups"]
            try:
                # find all the roles of those groups by query in the roles table
                for group in cognito_groups:
                    groups_roles_records = self.find_group_roles(group , db=db)
            except:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Could not query in the database"
                )

            # for every role that the group has check True in the
            # required_statments dictionary
            for g_r in groups_roles_records:
                cur_statments_list = self.get_role_statements(g_r.role_id , db=db)
                for s in cur_statments_list:
                    if s in self.required_statements:
                        self.required_statements[s] = True
                    # special "all" symbol
                    if "*" in s:
                        resource = s.split(":")[0]
                        for rs in self.required_statements:
                            if resource in rs:
                                self.required_statements[rs] = True
                
            
            # make sure that all the statements checks as True at the required_statments
            self.validate_required_statements()

            # if the validate_required_statements did'nt raise any exception
            return jwt_creds
                

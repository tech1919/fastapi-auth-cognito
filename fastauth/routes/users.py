from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastauth.db_connection import get_db
from fastauth.permission import CognitoJWTPermissionCheck
from fastauth.models import User
from fastauth.schemas.models import UserCreate , UserDelete , UserUpdate , UserCheck

from fastauth.utils.user_crud import (
    user_create,
    user_delete,
    user_get_all,
    user_get_one,
    user_get_one_by_username,
    user_update,
    user_assign_to_group,
    user_get_metadata,
    user_update_metadata,

)


router = APIRouter(tags=["Users"])


@router.post(
    "/create" , 
    status_code=status.HTTP_201_CREATED,
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:write"]))],
    ) # response_model=UserCreate
def create_user(
    record : UserCreate,
    db: Session = Depends(get_db),
):
  
    return user_create(db=db , record=record)

@router.get(
    "/list/all" , 
    status_code=status.HTTP_200_OK , 
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:read"]))],
    ) # response_model=List[UserCreate]
def get_all_users(
    db: Session = Depends(get_db),
):
    return user_get_all(db=db)

@router.get(
    "/get-by-username/{username}", 
    status_code=status.HTTP_200_OK, 
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:read"]))],
    ) # response_model=UserCreate
def get_by_username(
    username : str, 
    db: Session = Depends(get_db)
    ):
    return user_get_one_by_username(db=db, username=username)

@router.get(
    "/get-by-id/{id}", 
    status_code=status.HTTP_200_OK, 
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:read"]))],
    ) # response_model=UserCreate
def get_by_id(
    id, 
    db: Session = Depends(get_db)
    ):
    return user_get_one(db=db, id=id)


@router.get(
    "/get/metadata/{id}" , 
    status_code=status.HTTP_200_OK,
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:read"]))],
    )
def get_user_metadata(id , db : Session = Depends(get_db)):
    return user_get_metadata(id=id , db=db) 

@router.put(
    "/update/metadata/{id}" , 
    status_code=status.HTTP_200_OK,
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:read"]))],
    )
def update_user_metadata(id , metadata : dict , db : Session = Depends(get_db)):
    return user_update_metadata(id=id , db=db , metadata=metadata)

@router.put(
    "/update" , 
    status_code=status.HTTP_200_OK ,
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:write" , "user:read"]))], 
    ) # response_model=UserCreate
def update_user(
    record : UserUpdate,
    db: Session = Depends(get_db),    
):
    return user_update(db=db , record=record)

@router.delete(
    "/delete/{id}" , 
    status_code=status.HTTP_200_OK , 
    response_model=UserDelete,
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:delete"]))],
)
def delete_user(
    id,
    db : Session = Depends(get_db),
):
    return user_delete(db=db , id=id)

@router.post(
    "/assign-to-group/{user_id}/{group_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies= [Depends(CognitoJWTPermissionCheck(statements=["user:write" , "user:read" , "group:read" , "group:write"]))],
)
def assign_user_to_group(
    user_id : UUID,
    group_id : UUID,
    db : Session = Depends(get_db),
):

    return user_assign_to_group(db=db , user_id=user_id , group_id=group_id)



        
    
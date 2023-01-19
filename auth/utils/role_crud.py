from uuid import UUID
from sqlalchemy.orm import Session

from auth.models import Role
from auth.schemas.models import (
    RoleCreate , 
    RoleUpdate , 
    RoleDelete ,
    Permission,
)


def has_permission(role : RoleUpdate , resource : str , action : str) -> bool:
    """
        This function check if a given role has a permission
        return True is it has and False if not
    """
    for s in role.permissions["statments"]:
        if s["resource"] == resource:
            for a in s["actions"]:
                if action == a:
                    return True
    
    return False

def role_create(db : Session , record : Role):
    db_record = Role(
        name=record.name, 
        permissions= record.permissions,
        )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def role_get_all(db: Session):
    return db.query(Role).all()

def role_get_one(db: Session , id : UUID):
    return db.query(Role).filter_by(id=id).one()

def role_add_a_permission(
    db : Session , 
    role_id : UUID , 
    permission : Permission,
    ):

    db_record = db.query(Role).filter_by(id = role_id).first()

    try:
        # adding to the list of statments
        db_record.permissions["statements"] += permission.statements
    except:
        # if the list is empty - declare as a list
        db_record.permissions["statements"] = permission.statements
    finally:

        # update the role
        return role_update(db=db , record=db_record)
        
def role_remove_a_permission(
    db : Session , 
    role_id : UUID , 
    permission : Permission, 
    ):

    db_record = db.query(Role).filter_by(id = role_id).first()

    # Permission has a field of statements that is a list of strings
    for statement in permission.statements:
        if statement in db_record.permissions["statements"]:
            db_record.permissions["statements"].remove(statement)
        
    # update the role
    return role_update(db=db , record=db_record)

def role_update(db: Session , record : RoleUpdate):
    update_query = {
        Role.name : record.name ,
        Role.permissions : record.permissions ,
        }
    db.query(Role).filter_by(id=record.id).update(update_query)
    db.commit()
    return db.query(Role).filter_by(id=record.id).one()

def role_delete(db : Session , id : UUID):
    record = db.query(Role).filter_by(id = id).all()
    if not record:
        return RoleDelete(message = "Record does not exists")
    db.query(Role).filter_by(id = id).delete()
    db.commit()
    return RoleDelete(message = "Record deleted")

from uuid import UUID
from sqlalchemy.orm import Session
from auth.models import Group , GroupUser , RolesEntities
from auth.schemas.models import GroupCreate , GroupUpdate , GroupDelete

from datetime import datetime

def group_create(db : Session , record : Group):
    db_record = Group(
        name=record.name,
        )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def groups_get_all(db: Session):
    return db.query(Group).all()

def group_get_one(db: Session , id : UUID):
    return db.query(Group).filter_by(id=id).one()

def group_update(db: Session , record : GroupUpdate):
    update_query = {
        Group.name : record.name,
        }
    db.query(Group).filter_by(id=record.id).update(update_query)
    db.commit()
    return db.query(Group).filter_by(id=record.id).one()

def group_delete(db : Session , id : UUID):
    record = db.query(Group).filter_by(id = id).all()
    if not record:
        return GroupDelete(message = "Record does not exists")
    db.query(Group).filter_by(id = id).delete()
    db.commit()
    return GroupDelete(message = "Record deleted")


def group_add_a_user(db : Session , user_id : UUID , group_id : UUID , expiry_date : datetime = None):

    try:
        # check if already exists
        record = db.query(GroupUser).filter(
            GroupUser.user_id == user_id ,
            GroupUser.group_id == group_id,
            ).one()
        return {"message" : "This user is already assign to this group"}
    except:

        db_record = GroupUser(
            group_id = group_id,
            user_id = user_id,
            expiry_date = expiry_date
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
        



def group_add_a_role(db : Session , role_id : UUID , cognito_group_name : str , expiry_date : datetime = None):
    
    try:
        # check if already exists
        record = db.query(RolesEntities).filter(
            RolesEntities.role_id == role_id ,
            RolesEntities.cognito_group_name == cognito_group_name,
            ).one()
        return {"message" : "This role is already assign to this group"}
    except:
        db_record = RolesEntities(
            cognito_group_name = cognito_group_name,
            role_id = role_id,
            expiry_date = expiry_date
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    
        

def group_remove_a_user(db : Session , user_id : UUID , group_id : UUID):

    record = db.query(GroupUser).filter(
        GroupUser.user_id == user_id ,
        GroupUser.group_id == group_id,
        ).one()
    if not record:
        return GroupDelete(message = "Record does not exists")

    db.query(GroupUser).filter(
        GroupUser.user_id == user_id ,
        GroupUser.group_id == group_id,
        ).delete()

    db.commit()
    return GroupDelete(message = "Record deleted")

def group_remove_a_role(db : Session , role_id : UUID , group_name : str):

    record = db.query(RolesEntities).filter(
        RolesEntities.role_id == role_id ,
        RolesEntities.cognito_group_name == group_name,
        ).one()
    if not record:
        return GroupDelete(message = "Record does not exists")

    db.query(RolesEntities).filter(
        RolesEntities.role_id == role_id ,
        RolesEntities.cognito_group_name == group_name,
        ).delete()

    db.commit()
    return GroupDelete(message = "Record deleted")

from uuid import UUID

from sqlalchemy.orm import Session

from auth.models import User , Group ,GroupUser
from auth.schemas.models import UserUpdate , UserCreate , UserDelete , UserCheck

from datetime import datetime

def user_create(db : Session , record : User):
    db_record = User(
        # name=record.name, 
        # email=record.email,
        cognito_id=record.cognito_id,
        hased_password=record.hased_password,
        is_active = record.is_active,
        is_superuser = record.is_superuser,
        is_verified = record.is_verified,
        )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def user_get_all(db: Session):
    return db.query(User).all()

def user_get_one(db: Session , id : UUID):
    return db.query(User).filter_by(id=id).one()

def user_get_metadata(db: Session , id : UUID):
    record = db.query(User).filter_by(id = id).one()
    return record.user_metadata

def user_update_metadata(db : Session , id : UUID , metadata : dict):
    record = user_get_one(db=db , id=id)
    record.user_metadata = metadata
    db.commit()
    record = user_get_one(db=db , id=id)
    return record

def user_update(db: Session , record : UserUpdate):
    update_query = {
        # User.name : record.name ,
        # User.email : record.email ,
        User.hased_password : record.hased_password ,
        User.is_active : record.is_active ,
        User.is_superuser : record.is_superuser ,
        User.is_verified : record.is_verified ,        
        }
    db.query(User).filter_by(id=record.id).update(update_query)
    db.commit()
    return db.query(User).filter_by(id=record.id).one()

def user_delete(db : Session , id : UUID):
    record = db.query(User).filter_by(id = id).all()
    if not record:
        return UserDelete(message = "Record does not exists")
    db.query(User).filter_by(id = id).delete()
    db.commit()
    return UserDelete(message = "Record deleted")

def user_assign_to_group(db : Session , user_id : UUID , group_id : UUID , expiry_date : datetime = None):
    db_record = GroupUser(
        group_id = group_id,
        user_id = user_id,
        expiry_date = expiry_date
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from database.connection import get_db
from auth.schemas.models import GroupDelete , GroupCreate , GroupUpdate

from auth.utils.group_crud import (
    group_create,
    group_delete,
    group_get_one,
    group_update,
    groups_get_all,
    group_add_a_user,
    group_add_a_role,
    group_remove_a_role,
    group_remove_a_user,
)

router = APIRouter(tags=["Groups"])



@router.post("/create" , status_code=status.HTTP_201_CREATED) # response_model=UserCreate
def create_group(
    record : GroupCreate,
    db: Session = Depends(get_db),
):
  
    return group_create(db=db , record=record)

@router.get("/list/all" , status_code=status.HTTP_200_OK , ) # response_model=List[UserCreate]
def get_all_groups(
    db: Session = Depends(get_db),
):
    return groups_get_all(db=db)

@router.get("/get/{id}", status_code=status.HTTP_200_OK, ) # response_model=UserCreate
def get_one_group(id, db: Session = Depends(get_db)):
    return group_get_one(db=db, id=id)

@router.put("/update" , status_code=status.HTTP_200_OK , ) # response_model=UserCreate
def update_group(
    record : GroupUpdate,
    db: Session = Depends(get_db),    
):
    return group_update(db=db , record=record)

@router.delete(
    "/delete/{id}" , 
    status_code=status.HTTP_200_OK , 
    response_model=GroupDelete
)
def delete_group(
    id,
    db : Session = Depends(get_db),
):
    return group_delete(db=db , id=id)

@router.post(
    "/add-a-user/{user_id}/{group_id}",
    status_code=status.HTTP_201_CREATED,
)
def assign_user_to_group(
    user_id : UUID,
    group_id : UUID,
    db : Session = Depends(get_db),
):

    return group_add_a_user(db=db , user_id=user_id , group_id=group_id)

@router.post(
    "/add-a-role/{role_id}/{cognito_group_name}",
    status_code=status.HTTP_201_CREATED,
)
def assign_role_to_group(
    role_id : UUID,
    cognito_group_name : str,
    db : Session = Depends(get_db),
):

    return group_add_a_role(db=db , role_id=role_id , cognito_group_name=cognito_group_name)

@router.delete(
    "/remove-a-user/{user_id}/{group_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
def remove_user_from_group(
    user_id : UUID ,
    group_id : UUID ,
    db : Session = Depends(get_db)
):

    return group_remove_a_user(db=db , user_id=user_id , group_id=group_id)

@router.delete(
    "/remove-a-role/{role_id}/{group_name}",
    status_code=status.HTTP_202_ACCEPTED,
)
def remove_role_from_group(
    role_id : UUID ,
    group_name : str ,
    db : Session = Depends(get_db)
):

    return group_remove_a_role(db=db , role_id=role_id , group_name=group_name)


import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String , ForeignKey , Integer , JSON , Boolean , DateTime
from sqlalchemy.dialects.postgresql import UUID

from typing import AsyncGenerator
from datetime import datetime
from database.connection import Base, engine


########################
# Users                #
########################

class User(Base):

    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True , default = uuid.uuid4)
    # cognito_id = Column(UUID(as_uuid=True))
    cognito_id = Column(String)
    hased_password = Column(String , nullable = True)
    is_active = Column(Boolean , default = True)
    is_superuser  = Column(Boolean , default = False)
    is_verified  = Column(Boolean , default = True)
    creation_date = Column(DateTime , nullable=True , default = datetime.now())
    modify_date = Column(DateTime , nullable=True , default = datetime.now())
    user_metadata = Column(JSON , nullable=True)

########################
# Roles                #
########################

class Role(Base):

    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True , default = uuid.uuid4)
    name = Column(String(50))
    permissions = Column(JSON , default = {} , nullable = False)
    creation_date = Column(DateTime , nullable = False , default = datetime.now())
    modify_date = Column(DateTime , nullable = False , default = datetime.now())
    expiry_date = Column(DateTime , nullable = True)

class RolesEntities(Base):

    __tablename__ = "roles_entities"

    id = Column(UUID(as_uuid=True), primary_key=True , default = uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))
    # group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'))
    cognito_group_name = Column(String)
    expiry_date = Column(DateTime , nullable = True)

########################
# Groups               #
########################

class Group(Base):

    __tablename__ = 'groups'

    id = Column(UUID(as_uuid=True), primary_key=True , default = uuid.uuid4)
    name = Column(String)
    creation_date = Column(DateTime , nullable = False , default = datetime.now())

class GroupUser(Base):

    __tablename__ = "groups_users"

    id = Column(UUID(as_uuid=True), primary_key=True , default = uuid.uuid4)
    group_id =  Column(UUID(as_uuid=True), ForeignKey('groups.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    expiry_date  = Column(DateTime , nullable = True)

from fastapi import APIRouter , Depends
from fastauth.routes import (
    users,
    group_user,
    groups,
    roles,
    roles_entities,
    userpool,
)
from fastauth import permission

auth_router = APIRouter()

auth_router.include_router(router = users.router , prefix="/users")
auth_router.include_router(router = groups.router , prefix="/groups")
auth_router.include_router(router = roles.router , prefix="/roles")
auth_router.include_router(router = userpool.router , prefix="/cognito" )


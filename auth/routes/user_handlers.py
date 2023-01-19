from fastapi import APIRouter, Depends , Security
router = APIRouter(tags=["auth"])

# auth handel
from auth.JWTBearer import JWTBearer
from auth.auth import jwks
from auth.permission import PermissionCheck
from auth.permission import (
    users_read_permission_check,
    event_write_permission_check,
)


auth = JWTBearer(jwks)






@router.get("/secure/withpermissions", 
description="this route is an example for a secure route",
dependencies=[Depends(users_read_permission_check ) ,Depends(event_write_permission_check)],)
async def secure_with_permissions():
    
    return {"message" : "You have access"}


@router.get("/secure", 
description="this route is an example for a secure route",
dependencies=[Depends(auth)],)
async def secure():
    
    return auth.jwt_creds


@router.get("/not_secure",
description="this route is an example for a non secure route",
)
async def not_secure(

):
    return True


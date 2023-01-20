from fastapi import APIRouter, Depends , Security
router = APIRouter(tags=["auth"])

# auth handel
from auth.JWTBearer import JWTBearer
from auth.auth import jwks
from auth.permission import PermissionCheck



auth = JWTBearer(jwks)


@router.get("/secure/withpermissions", 
description="this route is an example for a secure route",)
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


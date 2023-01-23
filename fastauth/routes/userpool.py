from fastapi import APIRouter , Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import boto3
import os
from dotenv import load_dotenv
load_dotenv()


USER_POOL_ID = os.environ.get('COGNITO_POOL_ID')
COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')

security = HTTPBasic()

router = APIRouter(tags=["Cognito"])


@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    client = boto3.client('cognito-idp')
    try:
        response = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': credentials.username,
                'PASSWORD': credentials.password
            }
        )
        return response
    except client.exceptions.NotAuthorizedException as e:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    except client.exceptions.UserNotFoundException as e:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


"""
    If your user pool is configured to use JSON Web Tokens (JWT) 
    for authentication, the JWT will be included in the AuthenticationResult 
    field of the response from the admin_initiate_auth method. Specifically, the 
    JWT will be included in the IdToken field of the AuthenticationResult dictionary
"""
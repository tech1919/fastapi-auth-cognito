# Fastauth - Basic User Management Package


This package is a ready to use user authentication and autorization managment system, Using FastAPI, PostgreSQL, and AWS Cognito JWT based authentication.
> ## Install Package

```
pip install "git+https://github.com/tech1919/fastapi-auth-cognito.git"
```


> ## Configure Environment

Configure `.env` file:
```
USERS_DATABASE_URL=postgresql://username:password@host:port/database_name
COGNITO_REGION=
COGNITO_POOL_ID=
COGNITO_CLIENT_ID=
```

> ## Add the auth router to the FastAPI app

import:
```python
from fastauth.router import auth_router
from fastapi import FastAPI
```

define the app:
```python
app = FastAPI(
    title = "API's name"
)
```

include the auth router:
```python
app.include_router(router = auth_router , prefix="/auth")
```

This router comes with a built in auth configuration for every route.

> ## Add authentication dependency

import:
```python
from fastauth.permission import CognitoJWTPermissionCheck
```

add authentication and permission check to a route:
```python
@router.get("/secure", 
description="this route is an example for a secure route",
dependencies=[Depends(CognitoJWTPermissionCheck(statements=["resource:action"]))],)
async def secure() -> bool:
    
    return { "message" : "You have access" }
```

another way of adding authentication and permission dependency to a group of routes:
```python
# example
app.include_router(router=users.router , prefix="/users" , dependencies=[Depends(CognitoJWTPermissionCheck(statements=["resource:action"]))])
# by adding this dependency, now every route 
# expect a JWT that can be authenticaded with the JWKS from AWS Cognito
```

if a request that was sent to this route, contain in the **headers**: 
```
{
    "Authorization" : "Bearer some.json.webtoken"
}
```
than, the route will check first if this is an authenticated one comes from the AWS Cognito UserPool, as specified in the relevant environment variable `COGNITO_POOL_ID`. in this specific example , the route will also return the jwt cresentials as decoded from the JWT. this variable has this structure:
```json
{
  "jwt_token": "the original JWT string",
  "header": {
    "kid": "NkMpoZmqv4UBEWkN/yCvN/W2rSFnHRswDa6PjiyAUuc=",
    "alg": "RS256"
  },
  "claims": {
    "sub": "ec108666-34f7-4224-9ba7-89afe5aa6202",
    "cognito:groups": [
      "DEVELOPER"
    ],
    "iss": "https://cognito-idp.us-east-2.amazonaws.com/us-east-2_JA8KShbIm",
    "version": 2,
    "client_id": "7hn1v7k92bq9thva39l0floorm",
    "token_use": "access",
    "scope": "aws.cognito.signin.user.admin openid profile",
    "auth_time": 1671202410,
    "exp": 1671206010,
    "iat": 1671202410,
    "jti": "7e97bdaf-b074-4bc4-931b-cb50d72482ea",
    "username": "username string"
  },
  "signature": "the jwt signature string",
  "message": "some string"
}
```

So there is a lot of information here about the user who sent the request and with which you can later decide what is displayed in the client

> ## Handle Resources

For checking a user's permissions there is a class called `PermissionCheck`. This class depend on the authentication method so by adding this as a dependency to a certain route, it automaticly check the JWT authentication and user's permissions. 

Every route in the API that depends on this class will be obliged to perform authentication with the JWT sent to it, and then search the database according to the groups that appear in the JWT's payload under `cognito:groups` for all the roles associated with this group.





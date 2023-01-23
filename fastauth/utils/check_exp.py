from datetime import datetime
from fastapi import HTTPException 
from starlette.status import HTTP_403_FORBIDDEN

def has_expired(expiration_date = None , cognito_jwt = False) -> bool:

    """
        This function checks is a time stemp 
        has expired.
        returns True if has expired and False if not
    """

    if cognito_jwt:
        expiration_date = dict(cognito_jwt.claims)["exp"]
    if expiration_date == None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail= "Could not find experaion date"   
        )
        

    # Convert seconds since the epoch to a datetime object
    expiration_date = datetime.fromtimestamp(expiration_date)
    # Get the current date and time
    current_datetime = datetime.now()
    # Compare the expiration date with the current date and time
    if current_datetime > expiration_date:
        raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail= "Token has expired"    
            )
    else:
        return False

            
    

    
            

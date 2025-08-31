from datetime import datetime, timedelta, timezone
from authlib.jose import JoseError, jwt
from fastapi import HTTPException
from src.core.config import settings

def create_access_token(data: dict) -> str:
    """
    Create a JWT access token with expiration.
    `data` should include {"sub": username} or other payload info.
    """
    # Define the JWT header with algorithm and type
    header = {"alg": settings.ALGORITHM, "typ": "JWT"}
    
    # Calculate the expiration time for the token
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES)
    
    # Copy the input data and add the expiration timestamp to the payload
    payload = data.copy()
    payload.update({"exp": expire.timestamp()})  # Store expiration as a timestamp
    
    # Encode the token using the header, payload, and secret key
    token = jwt.encode(header, payload, settings.SECRET_KEY)
    
    # Return the encoded token as a string
    return token

def verify_token(token: str):
    """
    Verify the validity of a JWT token.
    Decode the token and validate its claims.
    """
    try:
        # Decode the token using the secret key
        claims = jwt.decode(token, settings.SECRET_KEY)
        
        # Validate the claims (e.g., check expiration, etc.)
        claims.validate()
        
        # Return the decoded claims if valid
        return claims
    except JoseError:
        # Raise an HTTP exception if the token is invalid
        raise HTTPException(status_code=401, detail="Could not validate credentials")
from datetime import datetime, timedelta, timezone
from authlib.jose import JoseError, jwt
from fastapi import HTTPException,status,Header
from src.core.config import settings
from typing import Optional

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
    
def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Extracts and verifies the current user from the 'Authorization' header (Bearer token).
    Raises an HTTPException if the token is missing, invalid, or expired.
    """
    if not authorization:
        # Raise an exception if the Authorization header is missing
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    
    try:
        # Split the Authorization header into scheme and token
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            # Raise an exception if the authentication scheme is not 'Bearer'
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")
    except ValueError:
        # Raise an exception if the Authorization header format is invalid
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")

    # Verify the token and extract the payload
    payload = verify_token(token)
    if not payload:
        # Raise an exception if the token is invalid or expired
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    # Return the payload containing user information
    return payload
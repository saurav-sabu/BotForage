from datetime import datetime,timedelta,timezone
from authlib.jose import JoseError,jwt
from fastapi import HTTPException
from src.core.config import settings

def create_access_token(data: dict) -> str:
    """
    Create a JWT access token with expiration.
    `data` should include {"sub": username} or other payload info.
    """
    header = {"alg": settings.ALGORITHM, "typ": "JWT"}
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES)
    payload = data.copy()
    payload.update({"exp": expire.timestamp()})  # store exp as timestamp
    token = jwt.encode(header, payload, settings.SECRET_KEY)
    return token  # already a string, no decode needed

def verify_token(token:str):
    try:
        claims = jwt.decode(token,settings.SECRET_KEY)
        claims.validate()
        username = claims.get("sub")
        if username is None:
            raise HTTPException(status_code=401,detail="Token is missing")
        return username
    except JoseError:
        raise HTTPException(status_code=401,detail="Could not validate credentials")
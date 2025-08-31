from fastapi import APIRouter, HTTPException, status, Depends, Header
from src.schemas.user_schemas import UserSignUp, UserResponse, UserSignIn
from src.services.user_services import create_user, get_user_by_email, get_all_users, verify_password
from typing import Optional
from src.core.security import create_access_token, verify_token

# Create a new API router for authentication-related routes
router = APIRouter()

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
    return payload

@router.post("/token")
def login(user: UserSignIn):
    """
    Authenticates a user by verifying their email and password.
    Returns an access token if the credentials are valid.
    """
    # Retrieve the user by email
    existing_user = get_user_by_email(user.email)
    if not existing_user or not verify_password(user.password, existing_user.password):
        # Raise an exception if the credentials are invalid
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    # Generate an access token for the authenticated user
    access_token = create_access_token({"sub": existing_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile")
def profile(user=Depends(get_current_user)):
    """
    Retrieves the profile of the currently authenticated user.
    """
    # Return the username from the token payload
    return {"username": user["sub"]}

# Route for user signup
@router.post("/signup", response_model=UserResponse)
def signup(user: UserSignUp):
    """
    Handles user signup by checking if the email is already registered.
    If not, creates a new user and returns the user details.
    """
    # Check if a user with the given email already exists
    existing_user = get_user_by_email(user.email)
    if existing_user:
        # Raise an HTTP exception if the email is already registered
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create a new user
    new_user = create_user(user)
    # Return the user details in the response
    return UserResponse(
        id=str(new_user.id),
        email=new_user.email,
        username=new_user.username,
        is_active=new_user.is_active
    )

# Route to get all users
@router.get("/get_users")
def list_users():
    """
    Retrieves and returns a list of all users.
    """
    # Fetch all users from the database
    users = get_all_users()
    # Return the list of users
    return users

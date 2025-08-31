from fastapi import APIRouter, HTTPException, status
from src.schemas.user_schemas import UserSignUp, UserResponse
from src.services.user_services import create_user, get_user_by_email, get_all_users
from typing import List

# Create a new API router for authentication-related routes
router = APIRouter()

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
@router.post("/get_users")
def get_user():
    """
    Retrieves and returns a list of all users.
    """
    # Fetch all users from the database
    users = get_all_users()
    # Return the list of users
    return users

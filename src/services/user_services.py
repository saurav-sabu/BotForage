from src.models.user_model import User
from src.schemas.user_schemas import UserSignUp, UserResponse
from src.core.hashing import hash_password, verify_password

# Function to create a new user
def create_user(user: UserSignUp):
    """
    Create a new user in the database.

    Args:
        user (UserSignUp): The user data for creating a new user.

    Returns:
        User: The newly created user object.
    """
    # Create a new User object with hashed password
    new_user = User(
        email=user.email,
        username=user.username,
        password=hash_password(user.password)  # Hash the user's password before saving
    )
    # Save the new user to the database
    new_user.save()
    return new_user

# Function to retrieve a user by their email
def get_user_by_email(email: str):
    """
    Retrieve a user from the database by their email.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        User: The user object if found, otherwise None.
    """
    # Query the database for a user with the given email
    return User.objects(email=email).first()

# Function to authenticate a user by email and password
def authenticate_user(email: str, password: str):
    """
    Authenticate a user by verifying their email and password.

    Args:
        email (str): The email of the user.
        password (str): The plain text password provided by the user.

    Returns:
        User: The authenticated user object if successful, otherwise None.
    """
    # Retrieve the user by email
    user = get_user_by_email(email)
    if not user:
        # Return None if the user does not exist
        return None
    # Verify the provided password against the stored hashed password
    if not verify_password(password, user.password):
        # Return None if the password is incorrect
        return None
    # Return the user object if authentication is successful
    return user

# Function to retrieve all users
def get_all_users():
    """
    Retrieve all users from the database.

    Returns:
        list[UserResponse]: A list of user response objects containing user details.
    """
    # Query the database for all users
    users = User.objects()
    user_list = []

    # Iterate through the users and create a response object for each
    for user in users:
        user_list.append(
            UserResponse(
                id=str(user.id),  # Convert the user ID to a string
                email=user.email,
                username=user.username,
                is_active=user.is_active  # Include the user's active status
            )
        )

    # Return the list of user response objects
    return user_list

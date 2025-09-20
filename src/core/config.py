from pydantic_settings import BaseSettings

# Define a Settings class that inherits from Pydantic's BaseSettings
class Settings(BaseSettings):

    # MongoDB connection URI, to be loaded from environment variables or .env file
    MONGODB_URI: str  # The connection string for MongoDB

    # Name of the database, to be loaded from environment variables or .env file
    DB_NAME: str  # The name of the MongoDB database

    # Secret key used for cryptographic operations (e.g., signing tokens)
    SECRET_KEY: str

    # Algorithm used for token encoding/decoding (e.g., HS256)
    ALGORITHM: str

    # Expiry time (in minutes) for access tokens
    ACCESS_TOKEN_EXPIRY_MINUTES: int

    # Cloudinary API key for authentication
    CLOUDINARY_API_KEY: str

    # Cloudinary cloud name identifier
    CLOUDINARY_CLOUD_NAME: str

    # Cloudinary API secret for secure access
    CLOUDINARY_API_SECRET: str

    GOOGLE_API_KEY: str

    # Configuration for the Settings class
    class Config:
        # Specify the .env file to load environment variables from
        env_file = ".env"

# Create an instance of the Settings class to access the configuration
settings = Settings()

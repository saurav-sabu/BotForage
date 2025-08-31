from pydantic_settings import BaseSettings

# Define a Settings class that inherits from Pydantic's BaseSettings
class Settings(BaseSettings):

    # MongoDB connection URI, to be loaded from environment variables or .env file
    MONGODB_URI: str
    # Name of the database, to be loaded from environment variables or .env file
    DB_NAME: str

    # Configuration for the Settings class
    class Config:
        # Specify the .env file to load environment variables from
        env_file = ".env"

# Create an instance of the Settings class to access the configuration
settings = Settings()

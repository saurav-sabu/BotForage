import mongoengine as me
from src.core.config import settings

# Function to initialize the MongoDB connection
def init_db():
    # Establish a connection to the MongoDB database using mongoengine
    me.connect(
        db=settings.DB_NAME,  # Name of the database to connect to
        host=settings.MONGODB_URI,  # MongoDB connection URI
        alias="default",  # Alias for the connection
        ssl=True,  # Enable SSL/TLS
        tlsAllowInvalidCertificates=False
    )

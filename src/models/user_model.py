import mongoengine as me

# Define the User model using MongoEngine's Document class
class User(me.Document):
    # Email field, must be unique and is required
    email = me.EmailField(required=True, unique=True)
    
    # Username field, must be unique and is required
    username = me.StringField(required=True, unique=True)
    
    # Password field, required for user authentication
    password = me.StringField(required=True)  # Fixed typo: changed 'stringField' to 'StringField'
    
    # Boolean field to indicate if the user is active, defaults to True
    is_active = me.BooleanField(default=True)

    # Metadata for the collection, specifying the collection name as 'users'
    meta = {"collection": "users"}

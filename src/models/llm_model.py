import mongoengine as me

# Define a MongoDB document model for storing LLM (Large Language Model) information
class LLM(me.Document):
    # Name of the model (e.g., GPT-3, GPT-4, etc.)

    model_name = me.StringField(required=True)
    
    # API key for accessing the model
    api_key = me.StringField(required=True)
    
    # API key for Pinecone (a vector database service)
    pinecone_api_key = me.StringField(required=True)
    
    # Name of the product associated with this model
    product_name = me.StringField(required=True)
    
    # URL endpoint for accessing the model
    url = me.StringField(required=True)
    
    # Optional field for storing a generated API key
    generated_url = me.StringField(null=True)

    # Metadata for the MongoDB collection name
    meta = {"collection": "llms"}

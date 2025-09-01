from fastapi import FastAPI
from src.db.mongodb import init_db
from src.routes import auth_routes, llm_routes

# Create an instance of the FastAPI application
app = FastAPI()

# Event handler to initialize the database connection when the application starts
@app.on_event("startup")
def start_db():
    # Initialize the database connection
    init_db()

# Include the authentication routes with a prefix and tag for better organization
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

# Include the LLM configs (Language Learning Model) routes with a prefix and tag for better organization
app.include_router(llm_routes.router1, prefix="/llm", tags=["LLM"])

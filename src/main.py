from fastapi import FastAPI
from src.db.mongodb import init_db
from src.routes import auth_routes, llm_routes , file_routes, prompt_routes
from fastapi.middleware.cors import CORSMiddleware

# Create an instance of the FastAPI application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Event handler to initialize the database connection when the application starts
@app.on_event("startup")
def start_db():
    # Initialize the database connection
    init_db()

# Include the authentication routes with a prefix and tag for better organization
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

# Include the LLM configs (Language Learning Model) routes with a prefix and tag for better organization
app.include_router(llm_routes.router1, prefix="/llm", tags=["LLM"])

# Include the file routes with a prefix and tag for better organization
app.include_router(file_routes.router2, prefix="/file", tags=["File"])

app.include_router(prompt_routes.router3,prefix="/prompt",tags=["Prompt"])
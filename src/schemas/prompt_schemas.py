from pydantic import BaseModel

class PromptRequest(BaseModel):
    business_ideas: str

class PromptResponse(BaseModel):
    system_prompt: str

from pydantic import BaseModel,HttpUrl
from typing import Optional

class LLMCreate(BaseModel):
    model_name:str
    api_key:str
    pinecone_api_key:str
    product_name:str
    url:HttpUrl
    generated_api:Optional[str] = None

class LLMUpdate(BaseModel):
    model_name:Optional[str] = None
    api_key:Optional[str] = None
    pinecone_api_key:Optional[str] = None
    product_name:Optional[str] = None
    url:Optional[HttpUrl] = None
    generated_api: Optional[str] = None

class LLMResponse(BaseModel):
    id:str
    model_name:str
    product_name:str
    url:HttpUrl
    generate_api:Optional[str]
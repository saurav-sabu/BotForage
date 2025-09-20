from fastapi import APIRouter, Depends, HTTPException
from src.schemas.prompt_schemas import PromptResponse,PromptRequest
from src.core.security import get_current_user
from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.config import settings


router3 = APIRouter()

@router3.post("/generate_system_prompt",response_model=PromptResponse)
def generate_system_prompt(request:PromptRequest,user=Depends(get_current_user)):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=settings.GOOGLE_API_KEY)
        instruction = f"""
        The user has a business: "{request.business_idea}".
        Generate a detailed system prompt for a RAG-based chatbot that will:
        - Represent this business
        - Use uploaded documents and vector database (RAG) to answer
        - Always stay professional, polite, engaging, and aligned with the brand
        - Be accurate and avoid hallucinations
        - If information is not in documents, politely say so
        """
        system_prompt = llm.predict(instruction)
        return PromptResponse(system_prompt=system_prompt)
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
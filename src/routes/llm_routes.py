from src.schemas.llm_schemas import LLMCreate, LLMResponse, LLMUpdate  # Importing schemas for request and response validation
from src.services.user_services import create_llm_records,update_llm_records  # Importing the service function to handle LLM record creation
from fastapi import APIRouter,Depends  # Importing FastAPI's APIRouter for route handling
from src.core.security import get_current_user

# Initialize a new APIRouter instance for handling routes related to LLM records
router1 = APIRouter()

@router1.post("/create_llm_records", response_model=LLMResponse)
def generate_llm_records(llm: LLMCreate,user=Depends(get_current_user)):
    """
    Endpoint to generate and store LLM records.
    
    Args:
        llm (LLMCreate): The input data required to create an LLM record.
    
    Returns:
        LLMResponse: The response containing the details of the created LLM record.
    """
    # Call the service function to create a new LLM record
    new_llm_record = create_llm_records(user["id"],llm)
    
    # Return the created LLM record details in the response
    return LLMResponse(
        user_id = str(new_llm_record.user_id),
        model_name=new_llm_record.model_name,  # Name of the LLM model
        api_key=new_llm_record.api_key,  # API key associated with the LLM
        pinecone_api_key=new_llm_record.pinecone_api_key,  # Pinecone API key for vector database
        product_name=new_llm_record.product_name,  # Name of the product using the LLM
        url=new_llm_record.url,  # URL associated with the LLM
        generated_url=new_llm_record.generated_url  # Generated API endpoint for the LLM
    )


@router1.post("/update_llm_records", response_model=LLMResponse)
def modify_llm_records(llm: LLMUpdate,user=Depends(get_current_user)):
    """
    Endpoint to generate and store LLM records.
    
    Args:
        llm (LLMCreate): The input data required to create an LLM record.
    
    Returns:
        LLMResponse: The response containing the details of the created LLM record.
    """
    # Call the service function to create a new LLM record
    updated_llm_records = update_llm_records(user["id"],llm)
    
    # Return the created LLM record details in the response
    return LLMResponse(
        user_id = str(updated_llm_records.user_id),
        model_name=updated_llm_records.model_name,  # Name of the LLM model
        api_key=updated_llm_records.api_key,  # API key associated with the LLM
        pinecone_api_key=updated_llm_records.pinecone_api_key,  # Pinecone API key for vector database
        product_name=updated_llm_records.product_name,  # Name of the product using the LLM
        url=str(updated_llm_records.url),  # URL associated with the LLM
        generated_url=updated_llm_records.generated_url  # Generated API endpoint for the LLM
    )
from fastapi import APIRouter,UploadFile,File,HTTPException,Depends
import cloudinary.uploader
from src.models.user_model import User
from src.core.config import settings
from src.core.security import get_current_user
from src.schemas.llm_schemas import LLMUpdate
from src.services.user_services import update_llm_records
import src.services.cloudinary_services

router2 = APIRouter()

@router2.post("/upload_pdf")
def upload_pdf(file: UploadFile = File(...),user=Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400,detail="Only PDF files are allowed")
    
    try:

        user_folder = f"user_pdfs/{user['id']}"

        upload_result = cloudinary.uploader.upload(
            file.file,
            resource_type="raw",
            public_id=file.filename,
            folder=user_folder
        )

        file_url = upload_result.get("secure_url")
        

        llm_update = LLMUpdate(url=str(file_url))
        updated_llm_record = update_llm_records(user["id"],llm_update)

        return {
            "message":"PDF Uploaded",
            "file_url":updated_llm_record.url,
            "folder":user_folder
        }
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
        

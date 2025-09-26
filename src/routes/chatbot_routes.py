from fastapi import APIRouter, Depends, HTTPException
from src.core.config import settings
from src.core.security import get_current_user
from src.services.langgraph_chatbot import *
from src.services.rag_ingestion import ingest_document_from_cloudinary
from src.models.llm_model import LLM  # MongoEngine Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from src.schemas.chat_schemas import ChatQuestion
from src.core.security import decrypt_api_key

router4 = APIRouter()

retriever_cache = {}

# -------------------------------
# Endpoint 1: Ingest PDF from MongoDB
# -------------------------------
@router4.post("/ingest_pdf_from_db")
def ingest_pdf_from_db(user=Depends(get_current_user)):
    try:
        # Query MongoEngine document
        llm_record = LLM.objects(user_id=str(user["id"])).first()
        if not llm_record or not llm_record.url:
            raise HTTPException(status_code=404, detail="PDF URL not found in DB")
        
        embedding_name = llm_record.embedding_name
        if not embedding_name:
            raise HTTPException(status_code=400, detail="Embedding Name not found for user")
        
        pinecone_api_key = decrypt_api_key(llm_record.pinecone_api_key)
        if not pinecone_api_key:
            raise HTTPException(status_code=400, detail="Pinecone API key not found for user")
        
        google_api_key = decrypt_api_key(llm_record.api_key)
        if not google_api_key:
            raise HTTPException(status_code=400, detail="Google API key not found for user")


        # Ingest PDF into Pinecone
        ingest_result = ingest_document_from_cloudinary(
            file_url=llm_record.url,
            user_id=str(user["id"]),
            embedding_name=embedding_name,
            pinecone_api_key=pinecone_api_key,
            google_api_key=google_api_key
        )


        return {
            "message": "PDF ingested successfully",
            "file_url": llm_record.url,
            "chunks_created": ingest_result.get("chunks", 0)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------
# Endpoint 2: Ask RAG Chat
# -------------------------------
@router4.post("/ask_rag_chat")
def ask_rag_chat(chatquestion: ChatQuestion, user=Depends(get_current_user)):

    try:
        llm_record = LLM.objects(user_id=str(user["id"])).first()
        if not llm_record or not llm_record.api_key or not llm_record.pinecone_api_key:
            raise HTTPException(status_code=400, detail="API keys not found for user")

        # Setup embedding & vectorstore
        embedding = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",  # correct embedding model
            google_api_key=llm_record.api_key
        )
        vectorstore = PineconeVectorStore(
            index_name="user-chatbot-index",
            embedding=embedding,
            pinecone_api_key=llm_record.pinecone_api_key
        )
        retriever = vectorstore.as_retriever(namespace=str(user["id"]))

        # Call chatbot
        answer = chat(
            question=chatquestion.question,
            system_prompt=chatquestion.system_prompt,
            retriever=retriever
        )

        print("Done with all")

        return {"question": chatquestion.question, "answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
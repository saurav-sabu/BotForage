import tempfile
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import PyPDFLoader
from src.core.config import settings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time

def ingest_document_from_cloudinary(file_url:str,user_id:str,embedding_name:str,pinecone_api_key:str,google_api_key:str):
    response = requests.get(file_url)
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp_file:
        tmp_file.write(response.content)
        local_path = tmp_file.name

    print("pdf downloaded to",local_path)

    loader = PyPDFLoader(local_path)
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    docs = text_splitter.split_documents(document)

    embedding = GoogleGenerativeAIEmbeddings(model=embedding_name,google_api_key=google_api_key)


    # 4. Initialize Pinecone client and check for index
    pc = Pinecone(api_key=pinecone_api_key)
    index_name = "user-chatbot-index"
        
    if not pc.has_index(index_name):
        pc.create_index(
                name=index_name,
                dimension=3072,  # Gemini embedding-001 dimension
                metric="cosine",  # Cosine similarity is a good default
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            # Give Pinecone some time to initialize the index
        while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)

        # 5. Initialize the PineconeVectorStore and ingest documents
    vectorstore = PineconeVectorStore(
            index_name=index_name,
            embedding=embedding,
            pinecone_api_key=pinecone_api_key
        )
    
    print("Done Successfully")

    vectorstore.add_documents(docs,namespace=user_id)

    print("Added Documents Successfully")

    return {"status":"Success","chunks":len(docs)}



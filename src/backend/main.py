from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router
import os
from rag_pipeline import insert_documents, CHROMA_DIR
from ait_logger import logger


chroma_path = os.path.join(os.path.dirname(__file__), CHROMA_DIR)
if not os.path.exists(chroma_path) or not os.listdir(chroma_path):
    logger.info("Chroma DB is empty, inserting documents...")
    insert_documents()

else:
    logger.info("Chroma DB already contains documents, skipping insertion.")


app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router from endpoints.py
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Home Page"}


print([route.path for route in app.routes])

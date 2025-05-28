from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.responses import StreamingResponse
import requests
from typing import List
from chat.chat import Chat
import json



router = APIRouter()


class ExampleDataInput(BaseModel):
    text: str

class ChatRequest(BaseModel):
    user_input: str

# Start chat instance
chat = Chat(
        topic="advanced distributed databases", 
        model_name="llama3.2:latest",
    )

@router.post("/uploadfile")
async def upload_pdf(files: List[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=400, detail=f"File {file.filename} is not a PDF."
            )

        contents = await file.read()
        uploaded_files.append({"filename": file.filename, "size": len(contents)})

    return {"uploaded": uploaded_files}



@router.post("/chat/stream")
async def chat_stream(user_input: str):
    # update internal context
    if not user_input:
        raise HTTPException(400, "user_input cannot be empty")

    async def event_generator():
        for chunk in chat.ask(user_input):
            yield json.dumps({"chunk": chunk}) + "\n"
        # once the model is done, send a final marker
        yield json.dumps({"done": True}) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson"
    )

@router.post("/examplePost")
async def examplePost(exampleData: exampleDataInput):
    # Replace this with your NLP pipeline later
    return {"message": f"Received syllabus with {len(exampleData.text)} characters"}


@router.get("/exampleGet")
async def example(exampleData: exampleDataInput):
    # Replace this with your NLP pipeline later
    return {"message": f"Received syllabus with {len(exampleData.text)} characters"}
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.responses import StreamingResponse
import requests
from typing import List
from chat.chat import Chat
from RAG.flashcards_generator import FlashcardsGenerator
from RAG.knowledge_base import KnowledgeBase
from RAG.Flashcards_llm_ollama import FlashCards
import json
from fastapi import Body, HTTPException





class ExampleDataInput(BaseModel):
    text: str

class ChatRequest(BaseModel):
    user_input: str

# Start chat instance
chat = Chat(
        topic="advanced distributed databases", 
        model_name="llama3.2:latest",
    )


kb = KnowledgeBase(
    collection_name="inf-3701"
)

# kb.build_collection("books")
print("KB built")


fg = FlashcardsGenerator(
    topic="advanced distributed databases",
    model_name="llama3:latest",
    knowledge_base=kb
    
)

fc= FlashCards(
    topic="advanced distributed databases",
    model_name="llama3.2:latest",
    k=3
    

)


router = APIRouter()



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
async def chat_stream(user_input: str = Body(..., embed=True)):
    if not user_input.strip():
        raise HTTPException(400, "user_input cannot be empty")

    def event_generator():
        for token in chat.ask(user_input):
            yield json.dumps({"chunk": token}) + "\n"
        yield json.dumps({"done": True}) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson",
        headers={
            # tell NGINX or other proxies not to buffer
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        },
    )

@router.post("/flashcards/create")
async def flashcards_create(user_input: str = Body(..., embed=True)):
    if not user_input:
        raise HTTPException(400, "user_input cannot be empty")
    try:
        user_input = int(user_input)
        if user_input <= 0:
            raise HTTPException(400, "Input must be a positive integer")
    except ValueError:
        raise HTTPException(400, "Wrong format on input. Please use a positive integer.")

    async def event_generator():
        for chunk in chat.ask(user_input):
            yield json.dumps({"stream": chunk}) + "\n"
        # once the model is done, send a final marker
        yield json.dumps({"done": True}) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson"
    )


@router.post("/flashcards/generate")
async def flashcards_generation(user_input: str = Body(..., embed=True)):
    if not user_input:
        raise HTTPException(400, "Input cannot be empty")
    
    try:
        user_input = int(user_input)
        if user_input <= 0:
            raise HTTPException(400, "Input must be a positive integer")
    except ValueError:
        raise HTTPException(400, "Wrong format on input. Please use a positive integer.")

    async def event_generator():
        try:
            flashcards = fg.generate_flashcards(user_input)
            for i, flashcard in enumerate(flashcards):
                yield json.dumps({"Flashcard num": i}) + "\n"
                yield json.dumps({"q": flashcard[0]}) + "\n"
                yield json.dumps({"a": flashcard[1]}) + "\n"
            yield json.dumps({"done": True}) + "\n"
        except Exception as e:
            # Log the error if needed
            yield json.dumps({"error": "Server error while generating flashcards."}) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson"
    )

from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Body
import json
from typing import List
from RAG.oral_examinator import OralExaminator
from starlette.responses import StreamingResponse
from chat.chat import Chat
from ait_logger import logger

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


class OralQuestionRequest(BaseModel):
    """Request model for generating oral questions.

    Args:
        BaseModel (pydantic.BaseModel): The base model class.
    """

    topic: str
    number_of_questions: int = 5


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


@router.get("/exampleGet")
async def example(exampleData: ExampleDataInput):
    # Replace this with your NLP pipeline later
    return {"message": f"Received syllabus with {len(exampleData.text)} characters"}


@router.post("/oral/questions")
async def generate_oral_questions(request: OralQuestionRequest):
    """Generate oral questions based on the provided topic.

    Args:
        request (OralQuestionRequest): The topic and number of questions.

    Raises:
        HTTPException: If question generation fails.

    Returns:
        List[str]: A list of generated oral questions.
    """
    examinator = OralExaminator(
        topic=request.topic, number_of_questions=request.number_of_questions
    )
    questions = examinator.generate_questions()

    return {"questions": questions}


@router.post("/oral/evaluate")
async def evaluate_oral_answer(
    topic: str = Form(...),
    question: str = Form(...),
    audio: UploadFile = File(...),
):
    """Evaluate a student's oral answer to a question.

    Args:
        topic (str, optional): The topic of the question.
        question (str, optional): The question being answered.
        audio (UploadFile, optional): The audio file containing the student's answer.

    Raises:
        HTTPException: If evaluation fails.

    Returns:
        str: The feedback on the student's answer, formatted as JSON.
    """
    examinator = OralExaminator(topic=topic)
    feedback = examinator.review_answer(question=question, student_answer=audio)

    try:
        return json.loads(feedback)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse feedback: %s", feedback)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse feedback: {feedback}",
        ) from exc


@router.post("/flashcards/create")
async def flashcards_create(user_input: str = Body(..., embed=True)):
    # update internal context
    if not user_input:
        raise HTTPException(400, "user_input cannot be empty")

    async def event_generator():
        for chunk in chat.ask(user_input):
            yield json.dumps({"stream": chunk}) + "\n"
        # once the model is done, send a final marker
        yield json.dumps({"done": True}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

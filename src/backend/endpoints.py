from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Body
import json
from typing import List
from examinator import Examinator
from starlette.responses import StreamingResponse
from chat.chat import Chat
from flashcards_generator import FlashcardsGenerator
from knowledge_base import KnowledgeBase
from Flashcards_llm_ollama import FlashCards
from game import get_ai_move, determine_result
from ait_logger import logger
from tts.text_to_speech import TextToSpeech
import io


class ExampleDataInput(BaseModel):
    text: str


class ChatRequest(BaseModel):
    user_input: str


class Move(BaseModel):
    user_move: str


# Start chat instance
chat = Chat(
    topic="advanced distributed databases",
    model_name="tinyllama:latest",
)


kb = KnowledgeBase(collection_name="inf-3701")

# kb.build_collection("books")
print("KB built")


fg = FlashcardsGenerator(
    topic="advanced distributed databases",
    model_name="llama3:latest",
    knowledge_base=kb,
)

fc = FlashCards(
    topic="advanced distributed databases", model_name="llama3.2:latest", k=3
)


router = APIRouter()


tts = TextToSpeech(voice="en-US-JennyNeural")


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
    examinator = Examinator(
        topic=request.topic, number_of_questions=request.number_of_questions
    )
    questions = examinator.generate_questions()

    return {"questions": questions}


@router.post("/evaluate/oral")
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
        dict: The feedback on the student's answer, formatted as JSON.
    """
    examinator = Examinator(topic=topic)
    feedback = examinator.review_oral_answer(question=question, student_answer=audio)

    try:
        return json.loads(feedback)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse feedback: %s", feedback)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse feedback: {feedback}",
        ) from exc


@router.post("/evaluate/text")
async def evaluate_text_answer(
    topic: str = Form(...),
    question: str = Form(...),
    student_answer: str = Form(...),
) -> dict:
    """Evaluate a student's text answer to a question.

    Args:
        topic (str, optional): The topic of the question.
        question (str, optional): The question being answered.
        student_answer (str, optional): The student's answer.

    Raises:
        HTTPException: If evaluation fails.

    Returns:
        dict: The feedback on the student's answer.
    """
    examinator = Examinator(topic=topic)
    feedback = examinator.review_text_answer(
        question=question, student_answer=student_answer
    )

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
    if not user_input:
        raise HTTPException(400, "user_input cannot be empty")
    try:
        user_input = int(user_input)
        if user_input <= 0:
            raise HTTPException(400, "Input must be a positive integer")
    except ValueError:
        raise HTTPException(
            400, "Wrong format on input. Please use a positive integer."
        )

    async def event_generator():
        for chunk in chat.ask(user_input):
            yield json.dumps({"stream": chunk}) + "\n"
        # once the model is done, send a final marker
        yield json.dumps({"done": True}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@router.post("/flashcards/generate")
async def flashcards_generation(user_input: str = Body(..., embed=True)):
    if not user_input:
        raise HTTPException(400, "Input cannot be empty")

    try:
        user_input = int(user_input)
        if user_input <= 0:
            raise HTTPException(400, "Input must be a positive integer")
    except ValueError:
        raise HTTPException(
            400, "Wrong format on input. Please use a positive integer."
        )

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
            yield json.dumps(
                {"error": "Server error while generating flashcards."}
            ) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@router.post("/tts/text-to-speech")
async def text_to_speech(text: str = Body(..., embed=True)):
    """Convert text to speech and return the audio file.

    Args:
        text (str, optional): The text to convert to speech.
    """
    if not text.strip():
        logger.warning("Received empty text for TTS conversion")
        raise HTTPException(400, "text cannot be empty")

    audio = await tts.text_to_speech(text)
    logger.info("TTS conversion completed successfully")

    return StreamingResponse(
        io.BytesIO(audio),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=output.mp3"},
    )


@router.post("/play")
def play(move: Move):
    ai_move = get_ai_move()
    result = determine_result(move.user_move, ai_move)
    return {"user_move": move.user_move, "ai_move": ai_move, "result": result}

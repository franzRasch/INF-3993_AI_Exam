from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from RAG.oral_examinator import OralExaminator


router = APIRouter()


class ExampleDataInput(BaseModel):
    text: str


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


@router.post("/examplePost")
async def examplePost(exampleData: ExampleDataInput):
    # Replace this with your NLP pipeline later
    return {"message": f"Received syllabus with {len(exampleData.text)} characters"}


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

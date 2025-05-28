from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from RAG.oral_examinator import OralExaminator


router = APIRouter()


class ExampleDataInput(BaseModel):
    text: str


class OralQuestionRequest(BaseModel):
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
    print(
        f"Generating {request.number_of_questions} questions for topic: {request.topic}"
    )
    examinator = OralExaminator(
        topic=request.topic, number_of_questions=request.number_of_questions
    )
    questions = examinator.generate_questions()

    print(f"Generated questions: {questions}")

    return {"questions": questions}

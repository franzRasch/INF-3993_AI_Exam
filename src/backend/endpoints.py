from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List


router = APIRouter()


class exampleDataInput(BaseModel):
    text: str


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
async def examplePost(exampleData: exampleDataInput):
    # Replace this with your NLP pipeline later
    return {"message": f"Received syllabus with {len(exampleData.text)} characters"}


@router.get("/exampleGet")
async def example(exampleData: exampleDataInput):
    # Replace this with your NLP pipeline later
    return {"message": f"Received syllabus with {len(exampleData.text)} characters"}

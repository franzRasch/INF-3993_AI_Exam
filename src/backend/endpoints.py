from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class exampleDataInput(BaseModel):
    text: str

@router.post("/examplePost")
async def examplePost(exampleData: exampleDataInput):
    # Replace this with your NLP pipeline later
    return {"message": f"Received syllabus with {len(exampleData.text)} characters"}

@router.get("/exampleGet")
async def example(exampleData: exampleDataInput):
    # Replace this with your NLP pipeline later
    return {"message": f"Received syllabus with {len(exampleData.text)} characters"}

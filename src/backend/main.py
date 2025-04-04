from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router  # Import the router from endpoints.py

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


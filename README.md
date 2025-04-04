# INF-3993_AI-Exam
## Contributors: Franz Ingebrigtsen, Marie Stenhaug and Skjalg Slubowski


# For developing
    1. Create a new venv
        python -m venv venv  # or 'python3' depending on the setup
    2. Activate the new venv
        Windows:
            .\venv\Scripts\activate
        Mac/Linux: 
            source venv/bin/activate
    3. Install dependencies
        pip install -r requirements.txt


    4 Run "node -v" to check for node js, if you dont have node: install it
    

## Backend

### Run backend
    uvicorn main:app --reload

### Access backend
    http://localhost:8000/

### Access backend api endpoints
    http://localhost:8000/docs


## Frontend

### Run frontend
    npm start
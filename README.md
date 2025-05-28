# INF-3993_AI-Exam

## Contributors: Franz Ingebrigtsen, Marie Alette Stenhaug and Skjalg Slubowski

## Tools

See [TOOLS.md](TOOLS.md) for a list of tools used in the project.

## Running the project

1. Create a new venv

   ```bash
   python -m venv venv  # or 'python3' depending on the setup
   ```

2. Activate the new venv
   Windows:

   ```bash
   .\venv\Scripts\activate
   ```

   Mac/Linux:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

   4 Run "node -v" to check for node js, if you don't have node: install it

### Backend

#### RAG for Flashcards generation
- **Ollama** CLI (used to run your local RAG model)
- **Model**: `llama3.2:latest`

 **Install Ollama**  
   macOS / Linux (Homebrew):  
   ```bash
   brew install ollama-ai/brew/ollama
   ```

#### Run backend

```bash
uvicorn main:app --reload
```

#### Access backend

```bash
http://localhost:8000/
```

#### Access backend api endpoints

```bash
http://localhost:8000/docs
```

### Frontend

#### Run frontend

```bash
npm start

```

Using qwen1.8b local model
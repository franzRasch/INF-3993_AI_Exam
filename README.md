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

   You also need to have `ffmpeg` installed.

   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`
   - **Windows**: Download from [FFmpeg](https://ffmpeg.org/download.html) and add it to your PATH.

4. Run "node -v" to check for node js, if you don't have node: install it


5. Run shell script for setting up and filling databases

   ```bash
   chmod +x setup.sh
   ```

   ```bash
   ./setup.sh
   ```

### Backend

#### RAG for Flashcards generation

- **Ollama** CLI (used to run your local RAG model)
- **Models**: `llama3.2:latest, llama3:latest, tinyllama:latest `

  **Install Ollama**
  macOS / Linux (Homebrew):

  ```bash
  brew install ollama-ai/brew/ollama
  ```
  **or**
  ```bash
  brew install ollama
  ```

  **for windows**
  go to https://ollama.com/download


#### Setup Ollama client using shell script
   ## After downloading Ollama run this script in a new terminal to setup client locally

   ```bash
   chmod +x setup_ollama.sh
   ```

   ```bash
   ./setup_ollama.sh
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

```

```

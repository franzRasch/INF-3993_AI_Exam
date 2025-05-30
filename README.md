# 🧠 INF-3993: AI Exam – AI Tutor (AIT)

**Contributors:** Franz Ingebrigtsen, Marie Alette Stenhaug & Skjalg Slubowski  
**Course:** INF-3993 – Generative AI

## 📁 Repository Structure

- `backend/` – FastAPI backend
- `frontend/` – React-based frontend UI
- `requirements.txt` – Python dependencies
- `TOOLS.md` – Documentation of AI models and libraries used

## 🛠️ Tools Used

A detailed list of tools and technologies used in this project is available in [`TOOLS.md`](TOOLS.md).

## 🚀 Getting Started

### 🔧 Setup Virtual Environment

1. **Create a new virtual environment:**

   ```bash
   python -m venv venv  # or 'python3' depending on your setup
   ```

2. **Activate the environment:**

   - **Windows:**

     ```bash
     .\venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install `ffmpeg` (required for audio processing):**

   - **macOS**:

   ```bash
     brew install ffmpeg
   ```

   - **Linux**:

   ```bash
     sudo apt install ffmpeg
   ```

   - **Windows**: You can install `ffmpeg` using one of the following methods:

   - Chocolatey: `choco install ffmpeg-full`
   - Scoop: `scoop install ffmpeg`
   - Winget: `winget install ffmpeg`

5. Run "node -v" to check for node js, if you don't have node: install it

### ⚙️ Backend Setup

#### 📚 Flashcard Generation via RAG

- **Local model inference via [Ollama](https://ollama.com/)**
- **Model:** `llama3.2:latest`

  **Install Ollama:**

  - **macOS** (Homebrew):

    ```bash
    brew install ollama-ai/brew/ollama
    ```

    - **Linux** (curl script):

    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```

    - **Windows**:  
      Download the installer from the official website:  
      [https://ollama.com/download](https://ollama.com/download)

#### ▶️ Run Backend

```bash
uvicorn main:app --reload
```

#### 📡 API Access

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Root endpoint: [http://localhost:8000/](http://localhost:8000/)

### 🖼️ Frontend Setup

Make sure you have **Node.js** installed (`node -v` to verify).  
If not, download it from [https://nodejs.org](https://nodejs.org)

#### ▶️ Run Frontend

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the development server:

   ```bash
   npm start
   ```

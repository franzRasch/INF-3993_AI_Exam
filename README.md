# 🧠 INF-3993: AI Exam – AI Tutor (AIT)

**Contributors:** Franz Ingebrigtsen, Marie Alette Stenhaug & Skjalg Slubowski  
**Course:** INF-3993 – Generative AI

## 📁 Repository Structure

- `backend/` – FastAPI backend
- `frontend/` – React-based frontend UI
- `requirements.txt` – Python dependencies
- `setup.sh` – Deployment script to prepare and populate the backend
- `setup_ollama.sh` – Script to configure Ollama with appropriate models
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

5. **Check Node.js:**

   ```bash
      node -v
   ```

   If not installed, download it from [https://nodejs.org](https://nodejs.org)

6. **Run shell script for setting up and filling the databases:**

   ```bash
   chmod +x setup.sh
   ```

   ```bash
   ./setup.sh
   ```

## ⚙️ Backend Setup

### 📚 Flashcard Generation via RAG

- **Local model inference via [Ollama](https://ollama.com/)**
- **Models:** `llama3.2:latest`, `llama3:latest`, `tinyllama:latest`, `qwen:1.8b`

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

#### 🛠️ Configure Ollama with setup script

After installing Ollama, run the following script to download and configure the models:

```bash
chmod +x setup_ollama.sh
./setup_ollama.sh
```

### ▶️ Run Backend

1. **Navigate to the backend directory:**

   ```bash
   cd src/backend
   ```

2. **Start the backend server using Uvicorn:**

   ```bash
   uvicorn main:app --reload
   ```

#### 📡 API Access

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Root endpoint: [http://localhost:8000/](http://localhost:8000/)

## 🖼️ Frontend Setup

1. **Install dependencies:**

   ```bash

   npm install
   ```

2. **Start the development server:**

   ```bash
   npm start
   ```

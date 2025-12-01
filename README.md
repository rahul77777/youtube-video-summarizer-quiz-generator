# 🎥 YouTube Quiz Generator

A full-stack Generative AI application that analyzes a YouTube video transcript and produces a structured **5-question multiple-choice quiz** in strict JSON format.

## ✨ Features

### ✅ Structured Output (Pydantic)
Uses **LangChain’s `PydanticOutputParser`** to enforce strict JSON schema, eliminating malformed responses and hallucinations.

### 🧠 Decoupled Architecture
- **FastAPI Backend** → AI logic (“The Brain”)  
- **Streamlit Frontend** → User-facing interface  
Clean separation makes the app scalable and modular.

### 🖥️ Streamlit Client
The UI communicates with the backend using REST via the `requests` library.

### 🎤 Transcript Extraction
Retrieves transcripts using **youtube-transcript-api**.

### 🔗 Modern LCEL Pipeline
Implements the LangChain Expression Language pattern:

```
Prompt | Model | Parser
```

## 🛠️ Technologies Used

| Category            | Technology                        | Purpose |
|--------------------|-------------------------------------|---------|
| Backend API        | FastAPI, Uvicorn                    | Provides `/generate_quiz` endpoint |
| Frontend UI        | Streamlit, requests                 | UI + API communication |
| AI Layer           | LangChain Core, LangChain OpenAI    | Prompt orchestration + LLM |
| Data Schema        | Pydantic                            | Enforces JSON quiz structure |
| Data Source        | youtube-transcript-api              | Transcript extraction |

## ⚠️ Developer Note: Transcript API Update

The old method is deprecated:

| Deprecated | Use Instead |
|-----------|-------------|
| `YouTubeTranscriptApi.get_transcript(video_id)` | `YouTubeTranscriptApi.fetch(video_id)` |

➡ Update the `get_transcript_text` function in `backend/ai_logic.py`.

## 🚀 Getting Started

You will run **two terminals simultaneously** — one for backend and one for frontend.

## 1. Prerequisites

Navigate to the project directory:

```
yt-quiz-generator/
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key in `.env`:

```
OPENAI_API_KEY=your_key_here
```

## 2. Run the Backend (FastAPI)

Open **Terminal 1**:

```bash
uvicorn backend.main:app --reload
```

Backend will be available at:

```
http://127.0.0.1:8000
```

## 3. Run the Frontend (Streamlit)

Open **Terminal 2**:

```bash
streamlit run frontend/app.py
```

A browser window will open where you can paste a YouTube URL and generate a quiz.

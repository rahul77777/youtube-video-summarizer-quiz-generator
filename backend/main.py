from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.ai_logic import generate_quiz_from_url

app = FastAPI(title="YouTube Quiz API", version="1.0")

# Input Schema (What the frontend sends us)
class QuizRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "Welcome to the YouTube Quiz API! Send POST requests to /generate_quiz"}

@app.post("/generate_quiz")
async def generate_quiz(request: QuizRequest):
    try:
        # Call our internal logic
        quiz_data = generate_quiz_from_url(request.url)
        return quiz_data
        
    except ValueError as e:
        # Handle known errors (e.g., no transcript found)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected server errors
        raise HTTPException(status_code=500, detail="Internal Server Error")


import os
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load env variables (API Keys)
load_dotenv()

# --- 1. Define the Data Structure (The "Shape" of the Output) ---
class Question(BaseModel):
    question_text: str = Field(description="The actual question text")
    options: List[str] = Field(description="List of 4 possible answers")
    correct_answer_index: int = Field(description="Index of the correct answer (0-3)")
    explanation: str = Field(description="Brief explanation of why this answer is correct")

class Quiz(BaseModel):
    title: str = Field(description="A catchy title for the quiz based on the video")
    questions: List[Question] = Field(description="List of 5 multiple choice questions")

# --- 2. Helper Functions ---
def extract_video_id(url: str) -> str:
    """Extracts the 'v' parameter from a YouTube URL."""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url:
        return url.split("/")[-1]
    return url  # Fallback if it's already an ID

def get_transcript_text(video_url: str) -> str:
    """Fetches and combines transcript text from YouTube."""
    try:
        video_id = extract_video_id(video_url)
        # Fetch transcript (returns a list of dictionaries)
        ytt_api = YouTubeTranscriptApi()
        captions = ytt_api.fetch(video_id)

        transcript_segments = []
        for line in captions:
            start_time = line.start
            duration = line.duration
            text = line.text
            timestamp = f"[{start_time:.2f}s-{start_time + duration:.2f}s]"
            transcript_segments.append(f"{timestamp} {text}")
        transcript_text = "\n".join(transcript_segments)
        return transcript_text
    except Exception as e:
        raise ValueError(f"Could not retrieve transcript: {str(e)}")

# --- 3. The Main Logic Chain ---
def generate_quiz_from_url(video_url: str) -> dict:
    # A. Get the Content
    transcript_text = get_transcript_text(video_url)
    
    # B. Initialize the Model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # C. Setup the Parser (Forces JSON)
    parser = PydanticOutputParser(pydantic_object=Quiz)
    
    # D. Create the Prompt
    template = """
    You are an expert educator. Your goal is to create a quiz based on the provided video transcript.
    
    Instructions:
    1. Analyze the transcript below.
    2. Create a quiz with exactly 5 multiple-choice questions.
    3. Ensure the questions test understanding of the key concepts.
    4. {format_instructions}
    
    Transcript:
    {transcript}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # E. The Chain: Prompt -> Model -> Parser
    chain = prompt | llm | parser
    
    # F. Execute
    try:
        # We inject the parser's instructions into the prompt automatically
        result = chain.invoke({
            "transcript": transcript_text[:15000], # Limit char count to avoid token limits
            "format_instructions": parser.get_format_instructions()
        })
        return result.model_dump() # Convert Pydantic object to standard Python dict
    except Exception as e:
        raise ValueError(f"Error generating quiz: {str(e)}")
import streamlit as st
import requests
import json

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/generate_quiz"

st.set_page_config(page_title="YouTube Quiz Generator", page_icon="📝")
st.title("📝 YouTube Quiz Generator")
st.markdown("Enter a YouTube URL below to generate a summary and a multiple-choice quiz.")

youtube_url = st.text_input(
    "YouTube Video URL:",
    placeholder="e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)

# --- Logic and API Call ---

if st.button("Generate Quiz") and youtube_url:
    if not ("youtube.com" in youtube_url or "youtu.be" in youtube_url):
        st.error("Please enter a valid YouTube URL.")
        st.stop()

    with st.spinner("Processing video and generating quiz... this may take up to 30 seconds."):
        try:
            response = requests.post(API_URL, json={"url": youtube_url})
            
            if response.status_code == 200:
                quiz_data = response.json()
                
                st.subheader(f"Quiz: {quiz_data.get('title', 'Generated Quiz')}")
                
                for i, q in enumerate(quiz_data.get('questions', [])):
                    with st.expander(f"**Question {i+1}:** {q['question_text']}", expanded=False):
                        
                        st.radio(
                            "Select your answer:",
                            q['options'],
                            index=None, 
                            key=f"q_{i}", 
                        )
                        st.success(f"**Correct Answer:** {q['options'][q['correct_answer_index']]}")
                        st.info(f"**Explanation:** {q['explanation']}")
                        
            elif response.status_code == 400:
                error_detail = response.json().get("detail", "Unknown error")
                st.error(f"Error 400: Could not process video. Detail: {error_detail}")
            else:
                st.error(f"API Error: Status {response.status_code}. Please check the backend console.")

        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Make sure your FastAPI server is running in a separate terminal!")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
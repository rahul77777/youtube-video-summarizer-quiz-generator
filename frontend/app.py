import streamlit as st
import requests
import json

# --- Configuration ---
# Your FastAPI server is running on this address
API_URL = "http://127.0.0.1:8000/generate_quiz"

st.set_page_config(page_title="YouTube Quiz Generator", page_icon="📝")
st.title("📝 YouTube Quiz Generator")
st.markdown("Enter a YouTube URL below to generate a summary and a multiple-choice quiz.")

# --- UI Input ---
youtube_url = st.text_input(
    "YouTube Video URL:",
    placeholder="e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)

# --- Logic and API Call ---

if st.button("Generate Quiz") and youtube_url:
    # 1. Input Validation
    if not ("youtube.com" in youtube_url or "youtu.be" in youtube_url):
        st.error("Please enter a valid YouTube URL.")
        st.stop()

    with st.spinner("Processing video and generating quiz... this may take up to 30 seconds."):
        try:
            # 2. Make the HTTP POST Request
            # We send the URL as a JSON payload to the FastAPI endpoint
            response = requests.post(API_URL, json={"url": youtube_url})
            
            # 3. Handle the Response
            if response.status_code == 200:
                quiz_data = response.json()
                
                # Render the Quiz (Success)
                st.subheader(f"Quiz: {quiz_data.get('title', 'Generated Quiz')}")
                
                for i, q in enumerate(quiz_data.get('questions', [])):
                    with st.expander(f"**Question {i+1}:** {q['question_text']}", expanded=False):
                        # Use Streamlit radio buttons for a clean presentation
                        
                        # Note: We display the options but the user only sees the result.
                        st.radio(
                            "Select your answer:",
                            q['options'],
                            index=None, # No default selection
                            key=f"q_{i}", 
                        )
                        # Display the correct answer in the expander for demonstration
                        st.success(f"**Correct Answer:** {q['options'][q['correct_answer_index']]}")
                        st.info(f"**Explanation:** {q['explanation']}")
                        
            elif response.status_code == 400:
                # Handle Bad Requests (e.g., No Transcript Error)
                error_detail = response.json().get("detail", "Unknown error")
                st.error(f"Error 400: Could not process video. Detail: {error_detail}")
            else:
                # Handle other server errors (e.g., 500 Internal Server Error)
                st.error(f"API Error: Status {response.status_code}. Please check the backend console.")

        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Make sure your FastAPI server is running in a separate terminal!")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
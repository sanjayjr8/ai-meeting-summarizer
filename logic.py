import streamlit as st
import whisper
import google.generativeai as genai
import sqlite3
from datetime import datetime
import json

# --- Database Functions ---
def init_db():
    """Initializes the database and creates the 'meetings' table with the correct schema."""
    conn = sqlite3.connect('meetings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            transcript TEXT,
            summary_json TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_meeting(filename, transcript, summary_json):
    """Saves a completed meeting summary and transcript to the database."""
    conn = sqlite3.connect('meetings.db')
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO meetings (filename, transcript, summary_json, created_at) VALUES (?, ?, ?, ?)",
        (filename, transcript, summary_json, created_at)
    )
    conn.commit()
    conn.close()

def load_meetings():
    """Loads all past meeting records from the database."""
    conn = sqlite3.connect('meetings.db')
    c = conn.cursor()
    c.execute("SELECT filename, summary_json, created_at, transcript FROM meetings ORDER BY created_at DESC")
    meetings = c.fetchall()
    conn.close()
    return meetings

# --- Core AI Logic Functions ---
@st.cache_data
def transcribe_audio(filepath, model_size="base"):
    """Transcribes an audio file using the selected Whisper model."""
    model = whisper.load_model(model_size)
    result = model.transcribe(filepath)
    return result["text"]

@st.cache_data
def summarize_text(_transcript, api_key):
    """Generates a structured JSON summary using the detailed, multi-part prompt."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    PROMPT = """
    You are an expert meeting summarizer and analyst with advanced skills in understanding structured and unstructured spoken-language transcripts. Your role is to transform the following meeting transcript into a clear, insight-rich summary.

    ---
    ### PRIMARY ANALYTICAL INSTRUCTIONS
    Your goal is to extract maximum meaning, clarity, and actionable insight from the transcript. You will analyze the content based on the following rules before formulating your final response.

    **1. Understanding and Precision:**
    - Read through the entire transcript before summarizing to grasp full context.
    - Identify speaker roles and topic shifts.
    - Merge fragmented or interrupted speech into coherent ideas.

    **2. Summarization Style:**
    - Be concise, objective, and factual. Paraphrase in a professional tone.
    - Limit the main summary to 6–10 sentences but ensure completeness.

    **3. Decisions Extraction:**
    - Include only confirmed decisions, not suggestions.
    - Start each decision with a strong action verb (e.g., Approved, Finalized, Agreed).
    - If a decision is conditional, mark it as *Pending confirmation*.

    **4. Action Items Extraction:**
    - Each action item must include an Owner, a Task, and a Deadline.
    - If the transcript lacks an owner or deadline, infer logically from context and mark any missing info as **(TBD)**.
    - Action items must start with a verb (e.g., Prepare, Review, Submit).

    **5. Handling Edge Cases:**
    - Ignore conversational fillers ("uh", "you know") and off-topic digressions.
    - Merge discussions on the same topic that occur at different times into one cohesive point.
    - If critical information is missing due to poor audio, mention "Information incomplete in transcript."

    ---
    ### CRITICAL OUTPUT REQUIREMENT
    
    After performing the detailed analysis above, your entire output **MUST BE A SINGLE, VALID JSON OBJECT** and nothing else.
    
    - Do **NOT** use Markdown headings (like '### Summary').
    - Do **NOT** add any introductory text, explanations, or closing remarks.
    - The response must start with `{` and end with `}`.

    The JSON object must have the following exact structure:
    {
        "summary": "A concise but comprehensive paragraph overview of the entire meeting.",
        "key_decisions": [
            "Decision 1...",
            "Decision 2..."
        ],
        "action_items": [
            {
                "owner": "Person or Team responsible",
                "task": "The specific action to be taken.",
                "deadline": "The deadline for the task, or (TBD)."
            }
        ]
    }
    ---

    Now, analyze the following transcript and provide the JSON output:
    """
    
    full_prompt = PROMPT + _transcript
    response = model.generate_content(full_prompt)
    
    json_response_text = response.text.strip().replace("```json", "").replace("```", "")
    return json_response_text

@st.cache_data
def query_text(_context, _user_prompt, api_key):
    """Sends a user's custom prompt and a context to the LLM for a direct answer."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    You are a helpful AI assistant. Based *only* on the text provided below, answer the user's question.
    
    --- TEXT CONTEXT ---
    {_context}
    --- END OF CONTEXT ---
    
    User's Question: "{_user_prompt}"
    """
    
    response = model.generate_content(prompt)
    return response.text
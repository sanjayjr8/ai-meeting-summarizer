import streamlit as st
import os
import json
from logic import init_db, save_meeting, load_meetings, transcribe_audio, summarize_text, query_text

# Initialize the database on the first run
init_db()

# --- Page Configuration ---
st.set_page_config(page_title="AI Meeting Summarizer", page_icon="🤖", layout="wide")

# --- Logo Placement ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Ensure you have a logo file at 'assets/logo.png'
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=200)
    else:
        st.warning("Logo not found. Place your logo at 'assets/logo.png'")

st.title("AI Meeting Summarizer 📋")

# --- Session State Initialization ---
# This ensures that data from the last uploaded file persists until a new one is processed.
if 'current_transcript' not in st.session_state:
    st.session_state.current_transcript = ""
if 'current_filename' not in st.session_state:
    st.session_state.current_filename = ""

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Options")
    model_size = st.selectbox(
        "Transcription Quality",
        ("tiny", "base", "small", "medium"),
        index=1,
        help="Select the AI model size for transcription. Larger models are more accurate but take significantly longer to process."
    )
    st.markdown("---")
    with st.expander("ℹ️ About This App"):
        st.write("""
            This app uses AI to automatically transcribe and summarize your meetings.
            - **Transcription:** Powered by OpenAI's Whisper model.
            - **Summarization:** Powered by Google's Gemini model.
            - **Interactive Chat:** Ask custom questions about your meetings.
            - **Database:** Meeting history is stored locally using SQLite.
        """)
    st.markdown("---")
    st.markdown("Built by **Sanjay J**")

# --- Main Page ---
st.markdown("Upload your meeting audio file to get a transcript, a concise summary, key decisions, and action items.")
st.info("Supported audio formats: MP3, WAV, M4A", icon="🎵")
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=['mp3', 'wav', 'm4a'],
    label_visibility="collapsed"
)

# --- Main Processing Logic ---
if uploaded_file is not None:
    st.header(f"Results for '{uploaded_file.name}'")
    
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner(f"1. Transcribing audio with '{model_size}' model... (This may take a while for large files)"):
        transcript_text = transcribe_audio(uploaded_file.name, model_size)
        st.session_state.current_transcript = transcript_text
        st.session_state.current_filename = uploaded_file.name

    with st.spinner("2. Generating summary with AI..."):
        summary_json = summarize_text(transcript_text, st.secrets["GEMINI_API_KEY"])
        try:
            summary_data = json.loads(summary_json)
            
            summary_tab, decisions_tab, actions_tab = st.tabs(["Summary", "Key Decisions", "Action Items"])

            with summary_tab:
                st.subheader("Meeting Summary")
                st.write(summary_data.get("summary", "No summary was generated."))

            with decisions_tab:
                st.subheader("Key Decisions Made")
                decisions = summary_data.get("key_decisions", [])
                if decisions:
                    for decision in decisions:
                        st.markdown(f"- {decision}")
                else:
                    st.write("No specific decisions were identified.")

            with actions_tab:
                st.subheader("Action Items")
                actions = summary_data.get("action_items", [])
                if actions:
                    for item in actions:
                        st.markdown(f"- **Owner:** {item.get('owner', 'N/A')} | **Task:** {item.get('task', 'N/A')} | **Deadline:** {item.get('deadline', 'N/A')}")
                else:
                    st.write("No specific action items were identified.")
            
            with st.expander("View Full Transcript"):
                st.code(transcript_text, language=None)
            
            save_meeting(uploaded_file.name, transcript_text, summary_json)
            st.success("Processing complete! Your summary has been saved to the history below.")

        except json.JSONDecodeError:
            st.error("The AI returned a summary in an unexpected format. Please check the raw response below.")
            st.write("Raw AI Response:")
            st.text(summary_json)
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            
    os.remove(uploaded_file.name)

# --- Interactive AI Features ---
st.markdown("---")

# Feature 1: Custom Query on Current Transcript
if st.session_state.current_transcript:
    st.header(f"🔍 Interact with '{st.session_state.current_filename}'")
    with st.expander("Ask a custom question about this specific meeting"):
        custom_question = st.text_input("e.g., 'What was the final decision on the budget?'", key="custom_q")
        if st.button("Get Custom Answer"):
            if custom_question:
                with st.spinner("Thinking..."):
                    answer = query_text(st.session_state.current_transcript, custom_question, st.secrets["GEMINI_API_KEY"])
                    st.info(answer)
            else:
                st.warning("Please enter a question.")

# Feature 2: Chat with Meeting History
st.header("💬 Chat with All Past Meetings")
past_meetings = load_meetings()
if not past_meetings:
    st.warning("Your meeting history is empty. Summarize a meeting to enable this feature.", icon="📁")
else:
    with st.expander("Ask a question across all previous meeting transcripts"):
        history_question = st.text_input("e.g., 'Have we ever discussed marketing budgets before?'", key="history_q")
        if st.button("Search History"):
            if history_question:
                with st.spinner("Searching through past meetings..."):
                    full_context = ""
                    for meeting in past_meetings:
                        filename, _, created_at, transcript = meeting
                        full_context += f"--- Meeting: {filename} ({created_at}) ---\n"
                        full_context += f"Transcript: {transcript}\n\n"
                    
                    answer = query_text(full_context, history_question, st.secrets["GEMINI_API_KEY"])
                    st.info(answer)
            else:
                st.warning("Please enter a question.")

# --- Meeting History Display ---
st.markdown("---")
st.header("🗂️ Meeting History")
if not past_meetings:
    st.info("Your saved summaries will appear here.")
else:
    for meeting in past_meetings:
        filename, summary_json_str, created_at, transcript = meeting
        with st.expander(f"**{filename}** - Summarized on: {created_at}"):
            try:
                summary_data = json.loads(summary_json_str)
                st.write("**Summary:**", summary_data.get("summary", "N/A"))
                st.write("**Full Transcript:**")
                st.info(transcript)
            except Exception as e:
                st.error("Could not display this summary due to a formatting issue.")
<div align="center">
  <img src="https://raw.githubusercontent.com/sanjayjr8/ai-meeting-summarizer/main/assets/logo.png" alt="App Logo" width="200"/>
  <h1>AI Meeting Summarizer</h1>
  <p>An intelligent web application that transcribes meeting audio and generates structured, action-oriented summaries, complete with interactive AI chat capabilities.</p>
  <p>
    <a href="https://meetinginsightengine.streamlit.app/"><strong>View Live Demo »</strong></a>
  </p>
</div>

<div align="center">
  <img src="YOUR_LINK_TO_A_GIF_DEMO_HERE.gif" alt="App Demo GIF"/>
</div>

<br>

This project was engineered to exceed the requirements of the hiring process for **Unthinkable Solutions**. It transforms raw meeting audio into a clear, actionable, and searchable knowledge base, demonstrating a deep understanding of full-stack AI application development.

---

## ✨ Core Features

This isn't just a summarizer; it's a complete meeting intelligence platform.

| Feature                    | Description                                                                                                                              | Benefit                                                                  |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Automated Transcription** | High-accuracy speech-to-text powered by **OpenAI's Whisper**. Users can select model quality to balance speed and precision.             | Eliminates manual note-taking and creates a perfect text record.         |
| **AI-Powered Summary** | Generates a structured output with a **Summary**, **Key Decisions**, and **Action Items** using a highly-detailed prompt for **Google Gemini**. | Instantly understand meeting outcomes and required actions.               |
| **Interactive AI Chat** | Ask custom questions about the current meeting or chat with the entire history of all summarized meetings to find cross-meeting insights. | Turns your meeting archive into a searchable, intelligent database.      |
| **Persistent History** | Every summary and transcript is automatically saved to a local **SQLite** database, creating a permanent and reviewable meeting log.     | Never lose track of past decisions or action items.                      |
| **Professional UI** | A clean, intuitive, and responsive interface built with **Streamlit**, featuring tabs and organized layouts for a seamless user experience. | Easy to use for both technical and non-technical users.                   |

---

## 🏗️ Architecture & Workflow

The application follows a logical, robust data processing pipeline designed for efficiency and clarity.

![Application Architecture Diagram](YOUR_LINK_TO_ARCHITECTURE_DIAGRAM_IMAGE_HERE.png)

1.  **Upload**: The user uploads an audio file via the Streamlit frontend.
2.  **Transcribe**: The audio is processed by the selected **Whisper** model to generate an accurate text transcript.
3.  **Analyze**: The transcript is sent to **Google Gemini** with a sophisticated, multi-part prompt that commands it to perform a detailed analysis.
4.  **Store**: The resulting summary and the full transcript are saved to the **SQLite** database with a timestamp.
5.  **Display & Interact**: The structured summary is presented in a clean, tabbed interface, and the user can now ask custom questions about the meeting.

---

## 💡 Technology Choices & Rationale

Every component was chosen to meet professional standards for quality, efficiency, and scalability. This directly addresses the **Technical Expectations** of the project.

| Component             | Technology                                                                                                    | Why It Was Chosen                                                                                                                                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend Framework** | **Streamlit** | For rapid development of a beautiful, interactive data science application with pure Python, enabling a focus on core logic over complex web development. |
| **ASR Engine** | **OpenAI Whisper** | Selected for its state-of-the-art transcription accuracy across a wide range of accents and audio qualities, directly addressing the accuracy requirement. |
| **LLM Engine** | **Google Gemini** | Chosen for its advanced reasoning capabilities and reliable, structured JSON output, which is essential for a stable application backend.               |
| **Data Persistence** | **SQLite** | Provides a zero-configuration, serverless, and robust SQL database. It perfectly fulfills the requirement for a backend that can **store and process data**.   |

---

## ✅ Fulfilling the Evaluation Focus

This project was built from the ground up to excel in the specific areas of evaluation.

### 1. Transcription Accuracy & Summary Quality
-   **Solution**: By integrating **Whisper**, a best-in-class ASR model, and **Gemini**, a top-tier LLM, the core output of the application is of the highest possible quality. The user-selectable model size for Whisper further demonstrates an understanding of the accuracy-vs-speed trade-off.

### 2. LLM Prompt Effectiveness
-   **Solution**: The project's "secret sauce" is its highly detailed, multi-part system prompt. It goes far beyond a simple request, acting as a comprehensive set of rules for the AI. This ensures consistent, high-quality, and structured output.

    <details>
    <summary>Click to view the prompt's core instructions</summary>

    ```
    You are an expert meeting summarizer and analyst... Your role is to transform the following meeting transcript into a clear, insight-rich summary...
    
    1. Understanding and Precision: Read through the entire transcript...
    2. Summarization Style: Be concise, objective, and factual...
    3. Decisions Extraction: Include only confirmed decisions...
    4. Action Items Extraction: Each action item must include an Owner, a Task, and a Deadline...
    5. Handling Edge Cases: Ignore conversational fillers...
    
    CRITICAL OUTPUT REQUIREMENT: Your entire output MUST BE A SINGLE, VALID JSON OBJECT...
    ```
    </details>

### 3. Code Structure
-   **Solution**: The codebase is logically partitioned into `app.py` for the user interface and `logic.py` for all backend processing (database, AI calls). This separation of concerns is a professional best practice that makes the code clean, scalable, and easy to maintain.

![Code Structure Diagram](YOUR_LINK_TO_CODE_STRUCTURE_IMAGE_HERE.png)

---

## 🚀 Getting Started Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/sanjayjr8/ai-meeting-summarizer.git](https://github.com/sanjayjr8/ai-meeting-summarizer.git)
    cd ai-meeting-summarizer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key:**
    -   Create a folder: `.streamlit`
    -   Inside it, create a file: `secrets.toml`
    -   Add your key: `GEMINI_API_KEY = "YOUR_KEY_HERE"`

5.  **Run the app:**
    ```bash
    streamlit run app.py
    ```
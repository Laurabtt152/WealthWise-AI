import streamlit as st
import re
from backend.app import generate_roadmap
from backend.roadmap_db import persist_roadmap
from backend.user_fin_quiz_response import insert_quiz_response

st.set_page_config(page_title="Financial Quiz", layout="centered")
st.title("🧠 Your FinQuiz")

# --- Ensure Required Data ---
if "demographics" not in st.session_state or "quiz_output" not in st.session_state:
    st.error("User demographics not found. Please fill that section first.")
    st.stop()

demographics = st.session_state["demographics"]
quiz_output = st.session_state["quiz_output"]

# --- Initialize Reset State ---
if "quiz_key_version" not in st.session_state:
    st.session_state.quiz_key_version = 0

# --- Quiz Rendering ---
pattern = r"## (.*?)\n(.*?)(?=\n## |\Z)"
matches = re.findall(pattern, quiz_output, re.DOTALL)
responses = {}

for section, questions_block in matches:
    st.subheader(section.strip())
    questions = re.findall(r"\d+\.\s+(.*)", questions_block)
    for idx, q in enumerate(questions):
        key_base = f"{section.strip()}_{idx}"
        key = f"{key_base}_v{st.session_state.quiz_key_version}"
        responses[key_base] = st.radio(q.strip(), ["Yes", "No"], key=key, index=None)

# --- Submit Answers and Generate Roadmap ---
if st.button("📨 Submit Quiz Answers"):
    for section, questions_block in matches:
        questions = re.findall(r"\d+\.\s+(.*)", questions_block)
        for idx, q_text in enumerate(questions):
            key_base = f"{section.strip()}_{idx}"
            ans = responses.get(key_base)
            if ans is not None:
                question_text = q_text.strip()
                success, msg = insert_quiz_response(
                    demographics.get("id"),
                    demographics.get("user_id", None),
                    question_text,
                    section.strip(),
                    ans == "Yes"
                )
                if not success:
                    st.error(f"Failed to insert: {msg}")

    st.success("✅ Responses submitted! Generating your personalized roadmap...")
    roadmap = generate_roadmap(demographics, responses)
    st.session_state.roadmap_data = roadmap

    if demographics.get("user_id") is not None:
        persist_roadmap(demographics.get("user_id"), roadmap)

    st.switch_page("pages/roadmap.py")

# --- Reset Quiz ---
if st.button("🔄 Reset Quiz"):
    st.session_state.quiz_key_version += 1
    st.rerun()

# --- Go Back to Demographics (data will be preserved!) ---
if st.button("🔙 Go Back"):
    st.switch_page("pages/demographics.py")

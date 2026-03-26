import streamlit as st
import re
from backend.app import generate_roadmap
from backend.roadmap_db import persist_roadmap
from backend.update_fin_quiz import update_fin_quiz

st.set_page_config(page_title="Financial Quiz", layout="centered")
st.title("🧠 Your Personalized Financial Quiz")

# --- Ensure Required Data ---
if "demographics" not in st.session_state or "quiz_questions" not in st.session_state:
    st.warning("Please fill out your demographics first.")
    st.stop()

demographics = st.session_state.demographics
quiz_questions = st.session_state.quiz_questions

# --- Initialize Reset State ---
if "quiz_key_version" not in st.session_state:
    st.session_state.quiz_key_version = 0

# --- Quiz Rendering ---
questions = st.session_state.quiz_questions
for question_id in questions.keys():
    question = list(questions[question_id])  # Convert tuple to list
    question[1] = (st.radio(question[4] + ' (' + question[5] + ')', ["Yes", "No"], key=question_id, index=None)) == "Yes"
    questions[question_id] = tuple(question)

# --- Submit Answers and Generate Roadmap ---
if st.button("📨 Submit Quiz Answers"):

    update_fin_quiz(questions)

    st.session_state.quiz_responses = questions
    st.success("✅ Responses submitted! Generating your personalized roadmap...")

    # Generate and store roadmap
    responses = {value[5]: value[4] for key, value in questions.items()}
    roadmap = generate_roadmap(demographics, responses)
    if demographics.get("user_id") is not None:
        persist_roadmap(demographics.get("user_id"), roadmap)
    st.session_state.roadmap_data = roadmap

    st.switch_page("pages/roadmap.py")

# --- Reset Quiz Selections ---
if st.button("🔄 Reset Quiz"):
    st.session_state.quiz_key_version += 1  # Forces radio button widget keys to update
    st.rerun()

# Optional: Back to Demographics
if st.button("🔙 Go Back"):
    st.switch_page("pages/demographics.py")

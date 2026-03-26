import streamlit as st
from PIL import Image
import pandas as pd
import os
import matplotlib.pyplot as plt
from utils.calendar import month_calendar
from datetime import date, timedelta
from utils.card import draw_course_card
from utils.standard_style import load_css
from utils.hide_streamlit_default import hide_default_info
from utils.page_config import setup_page_config
from utils.nav import draw_nav
from backend.get_user_info import fetch_quiz_questions, fetch_demographics
from backend.roadmap_db import fetch_roadmap


# Load in standard css
setup_page_config()
hide_default_info()
load_css()

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Initialize username if not present

if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is not None:
    st.session_state.quiz_questions = fetch_quiz_questions(st.session_state.username)
    st.session_state.demographics = fetch_demographics(st.session_state.username)
    st.session_state.roadmap_data = fetch_roadmap(st.session_state.username)
    if st.session_state.quiz_questions is not None and st.session_state.demographics and st.button("🚀 Take the FinQuiz again!", use_container_width=True):
        st.switch_page("pages/fin_quiz_retake.py")
    if st.session_state.roadmap_data is not None and st.button("🗺️ Your Personalized Financial Roadmap", use_container_width=True):
        st.switch_page("pages/roadmap.py")
else:
    st.button("🚀 Take the FinQuiz again!", use_container_width=True, disabled=True)
    st.button("🗺️ Your Personalized Financial Roadmap", use_container_width=True, disabled=True)

# ---- redirect guard -----------------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()


username = st.session_state.get("username", "User").split("@", 1)[0]

# ---------- HEADER ----------
st.markdown(f"## 👋 Welcome **{username}**")

# ---------- MAIN COLUMNS ----------
left, right = st.columns([3, 1], gap="large")

# -- LEFT: ROADMAP card -----------------
with left:
    st.markdown("### Your Roadmap")
    draw_course_card(
        title="Your Roadmap",
        subtitle="Personalized plan",
        chapters=6,
        items=56,
        progress=0,
        target_page="pages/roadmap.py",
    )

# -- RIGHT: REWARDS panel ---------------
with right:
    st.markdown("### 🎁 My Rewards")
    st.info("**Total points:** 300\n\nKeep learning to level-up!")

    # highlight last 5 days: green if done, red if missed
    last_five = {date.today().day-i: (i % 2 == 0) for i in range(5)}
    month_calendar(last_five)

# ---------- SEPARATOR ----------
st.markdown("---")

# ---------- ANALYTICS -----------
with st.container(key="feature-graphics"):
    col_l, col_r = st.columns(2, gap= "large")

    with col_l:
        st.image("assets/WW_ButtonClicked_Chart 1.png", use_container_width=True)

    with col_r:
        st.image("assets/WW_Finquiz_sentiments_Chart 1.png", use_container_width=True)
import streamlit as st
from pathlib import Path
from time import sleep
from utils.standard_style import load_css
from utils.hide_streamlit_default import hide_default_info
from utils.page_config import setup_page_config
from utils.nav import draw_nav

from backend.db_utils import authenticate_user
from backend.session_logger import log_login_session

# Configuration for the page
st.set_page_config(page_title="WealthWise | Login", layout="centered")

# Make the nav bar and setup default style.
setup_page_config()
hide_default_info()
load_css()
draw_nav()

# Redirect the user if they are already authenticated
if st.session_state.get("authenticated", False):
    # We will just go back to the landing page
    st.switch_page("pages/login_home_page.py")
    st.stop()
else:

    # Create a form
    with st.form("login_form", clear_on_submit=True):
        user = st.text_input(
            label = "email",
            max_chars = 255
        )
        pwd = st.text_input(
            "Password",
            max_chars = 100,
            type="password"
        )
        submit = st.form_submit_button(
            label = "Login"
        )
        st.page_link("pages/signup.py", label = "Don't have an account? Register")

    # Log the user in if their password was correct
    if submit:
        result = authenticate_user(user, pwd)
        if result["status"] == "success":
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.user_id = result["user_id"]

            session_id = log_login_session(result["user_id"])
            st.session_state.session_id = session_id  # Store for later logout tracking

            st.success("Login successful! Redirecting…")
            sleep(0.4)
            st.switch_page("pages/login_home_page.py")
        else:
            st.error(result["message"])

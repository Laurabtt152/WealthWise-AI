import streamlit as st
from PIL import Image
import os
from pathlib import Path
from utils.standard_style import load_css
from utils.hide_streamlit_default import hide_default_info
from utils.page_config import setup_page_config
from utils.nav import draw_nav
from deep_translator import GoogleTranslator

# Gather variables
logo = "assets/wealthwiselogo.png"
currency_img = "assets/Currency2.png"

def translate_text(text, lang):
    if lang == "en":
        return text
    return GoogleTranslator(source="auto", target=lang).translate(text)

LANGUAGES = {"English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr"}

# Language selection placeholder (🌐 icon dropdown)
language_container = st.container()
with language_container:
    language = st.selectbox(
        "",  # Label technically required but will be hidden
        LANGUAGES.keys(),
        index=list(LANGUAGES.values()).index("en"),
        key="language_dropdown"
    )

    selected_lang = LANGUAGES[language]
    st.markdown("""
    <style>
    /* Position dropdown fixed at top right */
    div[data-testid="stSelectbox"] {
        position: fixed;
        top: 15px;
        right: 20px;
        width: 60px;
        z-index: 9999;
    }

    /* Hide default label */
    div[data-testid="stSelectbox"] label {
        display: none !important;
    }

    /* Style the dropdown to just show the icon */
    div[data-baseweb="select"] > div {
        padding: 0px !important;
        min-height: 50px;
        width: 50px !important;
        justify-content: center;
        align-items: center;
        font-size: 26px;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        overflow: visible;
    }

    /* Add the 🌐 icon */
    div[data-baseweb="select"] > div:before {
        content: "🌐";
        font-size: 26px;
        display: block;
        line-height: 1;
    }

    /* Hide the dropdown arrow */
    div[data-baseweb="select"] svg {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


# Make the nav bar and setup default style.
setup_page_config()
hide_default_info()
load_css()
draw_nav()

# --- (everything above here stays the same) -------------------------
with st.container(key="main"):
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown(translate_text(
            "<h2 style='font-size:28px; font-weight:700;'>Discover Your Financial Fitness Level</h2>", selected_lang),
            unsafe_allow_html=True,
        )
        st.title(translate_text("How Financially Savvy Are You?", selected_lang))
        st.markdown(translate_text(
            """
            - **Personalized Feedback:** Receive honest insights into your financial knowledge.
            - **Tailored Learning Path:** Get a customized roadmap to enhance your financial skills.
            - **Empowerment:** Equip yourself with the tools to make informed financial decisions.
            """, selected_lang)
        )

        if st.button("Get Started", type="primary", use_container_width=True):
            st.switch_page("pages/demographics.py")

    with right_col:
        st.image(currency_img, width=500)

with st.container(key="feature-graphics"):
    col_l, col_r = st.columns(2, gap= "large")

    with col_l:
        st.image("assets/WW_ButtonClicked_Chart 1.png", use_container_width=True)

    with col_r:
        st.image("assets/WW_Finquiz_sentiments_Chart 1.png", use_container_width=True)


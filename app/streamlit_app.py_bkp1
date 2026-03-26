import streamlit as st
from PIL import Image
import os
from pathlib import Path
from utils.nav import draw_nav

st.set_page_config(
    page_title="WealthWise AI",
    page_icon = Image.open("assets/wealthwiselogo.png"),
    layout = "wide",
    initial_sidebar_state = "collapsed",
    menu_items = {'Get Help': None, 'Report a bug': None, 'About': None}
)

st.markdown("""
<style>
#MainMenu, header, footer,
.stDeployButton, .stAppDeployButton{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

logo = "assets/wealthwiselogo.png"
currency_img = "assets/currency.png"
# Load in CSS
css_path = Path("assets/styles/landing_page.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
else:
    print("Path for css was not found")

draw_nav("Welcome")

with st.container(key="main"):
    # --- 2-column layout ---
    left_col, right_col = st.columns([1, 1])

    # Center: Financial Savvy Info
    with left_col:
        st.markdown("<h2 style='font-size:28px; font-weight:700;'>Discover Your Financial Fitness Level</h2>", unsafe_allow_html=True)

        st.markdown("""
                    - **Personalized Feedback:** Receive honest insights into your financial knowledge.
                    - **Tailored Learning Path:** Get a customized roadmap to enhance your financial skills.
                    - **Empowerment:** Equip yourself with the tools to make informed financial decisions.
                    """)
        with st.container(key="start-journey"):
            st.page_link(page="pages/demographics.py", icon="🚀", label="Start Your Financial Journey")

    # Right: image
    with right_col:
        c = st.container(key="main-image")
        c.image(currency_img, width=300)

with st.container(key="analytics"):
    st.markdown("# Analytics Here")

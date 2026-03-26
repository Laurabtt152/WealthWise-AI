import streamlit as st
from time import sleep
from pathlib import Path
import datetime as dt
import re
import pycountry

from backend.db_utils import insert_user
from backend.fetch_from_db import fetch_from_cloud_sql
from utils.standard_style import load_css
from utils.hide_streamlit_default import hide_default_info
from utils.nav import draw_nav
from utils.page_config import setup_page_config
from backend.roadmap_db import persist_roadmap
 

# Get standard options
gender_options = ["", "Male", "Female", "Other", "Prefer not to say"]
countries =  [""] + sorted([country.name for country in pycountry.countries])

# Set up page style
setup_page_config()
hide_default_info()
load_css()
draw_nav()

# -------- NAV REDIRECT --------
if st.session_state.get("authenticated"):
    st.switch_page("../landing_page.py")   # already signed-in

# Define the user store
USERS = st.session_state.setdefault("user_store", {})


# -------- SIGN-UP FORM --------
st.title("Create your WealthWise account")

demographics = st.session_state.get("demographics") or {}

# Set default values (None if not present)
prefill_country = demographics.get("Country", "")
prefill_sex = demographics.get("Gender", "")
prefill_emp_st = demographics.get("Employment Status", None)
prefill_est_in = demographics.get("Estimated Income", None)
prefill_education = demographics.get("Education", None)


# Create the form
with st.form("signup", clear_on_submit=False):

    # Put the first/last name columns side by side
    col1, col2 = st.columns(2)
    first = col1.text_input("First name", max_chars = 40, placeholder = "John")
    last = col2.text_input("Last name",  max_chars = 40, placeholder = "Doe")

    sex = st.selectbox("Sex / Gender identity", options=gender_options,
                       index=gender_options.index(prefill_sex) if prefill_sex in gender_options else 0)

    # Get where the user is from
    country = st.selectbox("Country", options=countries,
                           index=countries.index(prefill_country) if prefill_country in countries else 0)

    # Get the user's birthday
    dob = st.date_input(
        "Date of birth",
        value = dt.date.today(),
        min_value = dt.date(1900, 1, 1),
        max_value = dt.date.today(),
    )

    age_ranges_dict = {age_label: age_id for age_id, age_label in fetch_from_cloud_sql('age_range')}
    age_labels = [""] + list(age_ranges_dict.keys())

    # --- Education Level ---
    education_levels_dict = {label: id for id, label in fetch_from_cloud_sql('education_level')}
    education_labels = [""] + list(education_levels_dict.keys())
    prefill_index = education_labels.index(
        prefill_education) if prefill_education in education_labels else 0
    selected_education_label = st.selectbox("🎓 Education Level",education_labels, index=prefill_index,key="education_level_select")
    selected_education_id = education_levels_dict.get(selected_education_label) if selected_education_label else None


    # --- Employment Status ---
    employment_statuses_dict = {label: id for id, label in fetch_from_cloud_sql('employment_status')}
    employment_labels = [""] + list(employment_statuses_dict.keys())

    prefill_index = employment_labels.index(
        prefill_emp_st) if prefill_emp_st in employment_labels else 0

    selected_employment_label = st.selectbox(
        "💼 Employment Status",
        employment_labels,
        index=prefill_index,
        key="employment_status_select"  # avoid duplicate key error
    )

    selected_employment_id = employment_statuses_dict.get(
        selected_employment_label) if selected_employment_label else None


    # --- Estimated Annual Income ---
    # Build the income options
    estimated_annual_income_dict = {label: id for id, label in fetch_from_cloud_sql('estimated_annual_income')}
    income_labels = [""] + list(estimated_annual_income_dict.keys())

    # Resolve index for preselected option
    prefill_index = income_labels.index(prefill_est_in) if prefill_est_in in income_labels else 0

    # Render selectbox with preselected value
    selected_income_label = st.selectbox(
        "💰 Estimated Annual Income",
        income_labels,
        index=prefill_index,
        key="estimated_income_select"
    )

    selected_income_id = estimated_annual_income_dict.get(selected_income_label) if selected_income_label else None


    email = st.text_input("Email", max_chars=120, placeholder="you@example.com")

    pwd  = st.text_input("Password", type="password", max_chars=100,
                         help="≥ 8 characters, one number & letter")
    pwd2 = st.text_input("Confirm password", type="password", max_chars=100)

    accept = st.checkbox("I accept the Terms & Privacy Policy")
    submit = st.form_submit_button("Create account")

# Validate the email through regex
def valid_email(x:str) -> bool:
    return re.fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", x) is not None

# This is what happens when the user presses create account
if submit:
    # Store the potential errors
    errors = []

    # Check for all errors
    if email in USERS:
        errors.append("email already exists.")
    if not valid_email(email):
        errors.append("Email address is not valid.")
    if len(pwd) < 8 or re.search(r"\d", pwd) is None or re.search(r"[A-Za-z]", pwd) is None:
        errors.append("Password must be ≥ 8 chars and contain letters & numbers.")
    if pwd != pwd2:
        errors.append("Passwords do not match.")
    if not accept:
        errors.append("You must accept the Terms.")

    # If errors are found, then print them to the user
    if errors:
        for e in errors:
            st.error(e)

    # Otherwise we will make a new user with their information
    # Here is where we will see what each user has. This will need
    # to match the JSON we define for an end user.
    else:
       # USERS[email] = {"password": pwd, "email": email, "first": first, "last": last}
        result = insert_user(first, last, email, pwd, sex[0], country, dob)

        # from INSERT RETURNING id
        if result["status"] == "success":
            user_id = result["user_id"]
            roadmap = st.session_state.roadmap_data
            persist_roadmap(user_id, roadmap)
            st.success("Account created! Redirecting to login …")
            sleep(0.6)
            st.switch_page("pages/login.py")
        else:
            st.error(result["message"])
import streamlit as st

def run_quiz():
    st.header("📊 Quick Financial Literacy Quiz")

    answers = {}
    answers['budgeting'] = st.radio("What is a budget?",
        ["Plan to manage income and expenses", "A type of loan", "Don't know"])
    answers['saving'] = st.radio("Why is saving important?",
        ["For emergencies", "To waste", "Not sure"])
    answers['credit'] = st.radio("What is a credit score?",
        ["A measure of trust to repay loans", "Your bank balance", "No idea"])
    answers['investing'] = st.radio("What does investing mean?",
        ["Growing money over time", "Losing money", "Not sure"])

    if st.button("Submit Quiz"):
        results = {
            "budgeting": "strong" if "Plan" in answers['budgeting'] else "weak",
            "saving": "strong" if "emergencies" in answers['saving'] else "weak",
            "credit": "strong" if "trust" in answers['credit'] else "weak",
            "investing": "strong" if "growing" in answers['investing'] else "weak"
        }
        return results
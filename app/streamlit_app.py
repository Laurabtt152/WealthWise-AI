import streamlit as st
from google import genai
from google.genai import types
from flask import Flask, request, jsonify
import os

client = genai.Client(
            vertexai=True,
            project="hack-team-off-the-ledger",
            location="europe-west1")


st.set_page_config(page_title="Gemini Chat", layout="centered")
st.title("🌟 Chat with Gemini Flash")

prompt = st.text_input("Enter your prompt:", "Tell me something amazing")

if st.button("Generate"):
    with st.spinner("Thinking..."):
        try:
            response = client.models.generate_content(model='gemini-2.0-flash-001',contents=prompt)
            st.success(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

# backend/db.py
import psycopg2
import streamlit as st

@st.cache_resource
def get_conn_params():
    return {
        "host": "34.74.95.159",
        "port": 5432,
        "database": "ledger-core-db",
        "user": "postgres",
        "password": "Ledger@2025"
    }

def get_conn():
    params = get_conn_params()
    return psycopg2.connect(**params)

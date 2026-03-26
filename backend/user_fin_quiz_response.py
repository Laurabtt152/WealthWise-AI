# db.py
import psycopg2
from datetime import datetime
import streamlit as st

from backend.db import get_conn




def insert_quiz_response(demographics_id, user_id, question_text, section_name, answer):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_fin_quiz_response (
                user_demographics_id, user_id, question_text, section_name, answer, answered_at
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            demographics_id,
            user_id,
            question_text,
            section_name,
            answer,
            datetime.now()
        ))

        conn.commit()
        return True, "Saved"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()
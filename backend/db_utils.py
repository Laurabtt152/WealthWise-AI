# db_utils.py
import bcrypt
import psycopg2

from backend.db import get_conn
import streamlit as st


def insert_user(first_name, last_name, email, password, sex, country, dob):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("""
                       INSERT INTO user_profile (first_name, last_name, email_address, password, sex, country, dob)
                       VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
                       """, (first_name, last_name, email, hashed_pw, sex, country, dob))
        user_id = cursor.fetchone()[0]

        # Link to existing demographics if present in session
        demographics_id = st.session_state.get("demographics", {}).get("id")
        if demographics_id:
            cursor.execute("""
                           UPDATE user_demographics
                           SET user_id = %s
                           WHERE id = %s;
                           """, (user_id, demographics_id))
            st.session_state.demographics["user_id"] = user_id  # Update session

            # ✅ Backfill quiz response records
            cursor.execute("""
                           UPDATE user_fin_quiz_response
                           SET user_id = %s
                           WHERE user_demographics_id = %s;
                           """, (user_id, demographics_id))

        conn.commit()
        return {"status": "success", "user_id": user_id}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return {"status": "error", "message": "Email already exists."}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()




def authenticate_user(email, password_input):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, password FROM user_profile WHERE email_address = %s", (email,))
        result = cursor.fetchone()

        if result:
            user_id, hashed_pw = result
            if bcrypt.checkpw(password_input.encode('utf-8'), hashed_pw.encode('utf-8')):
                return {"status": "success", "user_id": user_id}
            else:
                return {"status": "error", "message": "Invalid password."}
        else:
            return {"status": "error", "message": "User not found."}
    finally:
        cursor.close()
        conn.close()


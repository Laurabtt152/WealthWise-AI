from backend.db import get_conn
from datetime import datetime

def log_login_session(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_session_duration (user_id, login_time)
            VALUES (%s, %s)
            RETURNING id;
        """, (user_id, datetime.now()))
        session_id = cursor.fetchone()[0]
        conn.commit()
        return session_id
    except Exception as e:
        conn.rollback()
        print(f"Session log failed: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# backend/session_logger.py
import psycopg2
from backend.db import get_conn
from datetime import date

def log_user_session(session_id, login_time=None, logout_time=None):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_session_duration (session_id, login_time, logout_time)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (session_id, login_time, logout_time))
        session_row_id = cursor.fetchone()[0]
        conn.commit()
        return {"status": "success", "session_row_id": session_row_id}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()




def log_click_event(clickbutton, user_id=None, click_date=None):
    conn = get_conn()
    cursor = conn.cursor()

    if click_date is None:
        click_date = date.today()

    try:
        cursor.execute("""
            INSERT INTO clickdata (date, clickbutton, user_id)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (click_date, clickbutton, user_id))
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        return {"status": "success", "click_id": inserted_id}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()

import psycopg2
from backend.db import get_conn

def fetch_from_cloud_sql(table_name):
    conn = get_conn()  # ✅ Moved inside
    try:
        cursor = conn.cursor()
        sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Fetch error from {table_name}: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

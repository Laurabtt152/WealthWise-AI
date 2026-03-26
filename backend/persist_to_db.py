import psycopg2

# backend/persist_to_db.py

from backend.db import get_conn  # ✅ import your shared connection

def persist_to_cloud_sql(data: dict, table_name: str):
    conn = get_conn()
    cursor = conn.cursor()

    keys = data.keys()
    values = [data[k] for k in keys]
    placeholders = ', '.join(['%s'] * len(keys))
    columns = ', '.join(keys)

    query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        RETURNING id;
    """

    cursor.execute(query, values)
    inserted_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return inserted_id

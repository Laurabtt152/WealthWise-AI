import json
from backend.db import get_conn
from backend.get_user_info import get_user_id

def persist_roadmap(user_id, roadmap):
    conn = get_conn()
    cursor = conn.cursor()
    roadmap_json = json.dumps(roadmap)
    sql = "INSERT INTO roadmap (user_id, roadmap_content) VALUES (%s, %s)"
    cursor.execute(sql, (user_id, roadmap_json))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_roadmap(username):
    # Fetch the roadmap data from the database
    user_id = get_user_id(username)
    conn = get_conn()
    cursor = conn.cursor()
    sql = f"SELECT * FROM roadmap WHERE user_id = {user_id}"
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    row_data = [dict(zip(columns, row)) for row in rows][0] if rows else None
    if row_data:
        content = row_data['roadmap_content']
        if isinstance(content, memoryview):
            content = content.tobytes().decode('utf-8')
        return json.loads(content)
    return None
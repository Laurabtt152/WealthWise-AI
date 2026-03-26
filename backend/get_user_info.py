import psycopg2

def get_user_id(username):
    conn = psycopg2.connect(
        host='34.74.95.159',
        user='postgres',
        password='Ledger@2025',
        dbname='ledger-core-db'
    )
    cursor = conn.cursor()
    sql = f"SELECT id FROM user_profile where email_address = '{username}'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows[0][0] if rows and len(rows) > 0 else None


def fetch_quiz_questions(username):
    conn = psycopg2.connect(
        host='34.74.95.159',
        user='postgres',
        password='Ledger@2025',
        dbname='ledger-core-db'
    )
    cursor = conn.cursor()
    sql = f"SELECT * FROM user_fin_quiz_response where user_id = {get_user_id(username)}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {row[0]: row for row in rows}

def fetch_demographics(username):
    conn = psycopg2.connect(
        host='34.74.95.159',
        user='postgres',
        password='Ledger@2025',
        dbname='ledger-core-db'
    )
    cursor = conn.cursor()
    sql = f"SELECT * FROM user_demographics where user_id = {get_user_id(username)}"
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows][0] if rows else None
import psycopg2

def create_update_query(quiz_responses):
    set_clause = ' '.join([
        f"WHEN ID = {response} THEN {quiz_responses[response][1]}"
        for response in quiz_responses
    ])
    ids = ', '.join([str(response) for response in quiz_responses])
    sql = f"""
    UPDATE user_fin_quiz_response
    SET answer = CASE
        {set_clause}
        ELSE answer
    END
    WHERE ID IN ({ids});
    """
    print(sql)
    return sql

def update_fin_quiz(quiz_responses):
    conn = psycopg2.connect(
        host='34.74.95.159',
        user='postgres',
        password='Ledger@2025',
        dbname='ledger-core-db'
    )
    cursor = conn.cursor()
    sql = create_update_query(quiz_responses)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
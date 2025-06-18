def get_chat_history():
    import sqlite3
    conn = sqlite3.connect("Jarvis_database.db")
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            jarvis_response TEXT,
            response_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Fetch in order of `id` which is auto-incremented (more reliable than timestamp)
    cursor.execute("""
        SELECT user_query, jarvis_response 
        FROM memory 
        WHERE response_type = 'chat' 
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    chat_log = ""
    for user, jarvis in rows:
        chat_log += f"User: {user}\nJarvis: {jarvis}\n"
    return chat_log

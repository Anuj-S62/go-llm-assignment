import sqlite3
import threading


class DatabaseHandler:
    DB_PATH = '../app.db'

    def __init__(self):
        self.lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        with self.lock, sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    session_id TEXT,
                    column TEXT,
                    operation TEXT,
                    result REAL
                )
            """)
            conn.commit()

    def save_result(self, session_id, column, operation, result):
        try:
            with self.lock, sqlite3.connect(self.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        column TEXT,
                        operation TEXT,
                        result REAL
                    )
                """)
                conn.commit()
        except Exception as e:
            print(e)

    def fetch_results(self, session_id):
        with self.lock, sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM results WHERE session_id = ?", (session_id,))
            rows = cursor.fetchall()
        return [{"session_id": row[0], "column": row[1], "operation": row[2], "result": row[3]} for row in rows]

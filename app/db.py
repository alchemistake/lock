import sqlite3
from datetime import datetime
import os

def get_db_connection():
    db_path = os.environ.get('SQLITE_DB_PATH', 'clicks.db')
    conn = sqlite3.connect(db_path)
    return conn

def init_db():
    import os

    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS clicks
                (email TEXT, year INTEGER, month INTEGER, count INTEGER,
                PRIMARY KEY (email, year, month))"""
    )
    conn.commit()
    conn.close()

def increment_click(email):
    now = datetime.now()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO clicks (email, year, month, count) 
                VALUES (?, ?, ?, 1)
                ON CONFLICT(email, year, month) 
                DO UPDATE SET count = count + 1""",
        (email, now.year, now.month),
    )
    conn.commit()
    conn.close()

def get_clicks_data():
    conn = get_db_connection()
    c = conn.cursor()
    current_month = datetime.now().month
    current_year = datetime.now().year
    c.execute(
        """SELECT email, year, month, count FROM clicks
                WHERE year = ? AND month = ?
                ORDER BY count DESC""",
        (current_year, current_month)
    )
    data = c.fetchall()
    conn.close()
    return data

def get_user_total_clicks(email):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """SELECT SUM(count) FROM clicks WHERE email = ?""",
        (email,)
    )
    total_clicks = c.fetchone()[0] or 0
    conn.close()
    return total_clicks
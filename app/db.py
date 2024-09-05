import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("clicks.db")
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
    conn = sqlite3.connect("clicks.db")
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
    conn = sqlite3.connect("clicks.db")
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
    conn = sqlite3.connect("clicks.db")
    c = conn.cursor()
    c.execute(
        """SELECT SUM(count) FROM clicks WHERE email = ?""",
        (email,)
    )
    total_clicks = c.fetchone()[0] or 0
    conn.close()
    return total_clicks
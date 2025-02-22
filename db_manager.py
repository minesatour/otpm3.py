import sqlite3
import os

DB_PATH = "data/captured_otps.db"

def setup_database():
    """Create OTP database if it doesn't exist"""
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS otps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            otp TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_otp(otp):
    """Save captured OTP to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO otps (otp) VALUES (?)", (otp,))
    conn.commit()
    conn.close()

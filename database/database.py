import sqlite3

conn = sqlite3.connect('deadlines.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS deadlines (
id INTEGER PRIMARY KEY,
user_id TEXT,
title TEXT NOT NULL,
description TEXT,
date TEXT NOT NULL,
time TEXT NOT NULL,
reminder INTEGER NOT NULL
)
""")

conn.commit()
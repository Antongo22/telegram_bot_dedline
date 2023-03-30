import sqlite3

conn = sqlite3.connect('database/deadlines.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS deadlines (
id INTEGER PRIMARY KEY,
user_id TEXT,
title TEXT NOT NULL,
description TEXT,
date TEXT NOT NULL,
time TEXT NOT NULL,
ded_warning_date TEXT NOT NULL,
ded_warning_time TEXT NOT NULL
)
""")

conn.commit()
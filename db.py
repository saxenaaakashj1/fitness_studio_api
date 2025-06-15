import sqlite3
from datetime import datetime, timedelta
import pytz


# Establish a connection to the SQLite database
# 'check_same_thread=False' allows use of the connection across threads
# (useful in Flask apps)
connection = sqlite3.connect("fitness_studio.sqlite", check_same_thread=False)
cursor = connection.cursor()

# Create tables for classes and bookings if they don't already exist
cursor.executescript(
    """
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        datetime TEXT,
        instructor TEXT,
        available_slots INTEGER
    );

    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        client_name TEXT,
        client_email TEXT NOT NULL,
        booked_at TEXT,
        FOREIGN KEY(class_id) REFERENCES classes(id),
        UNIQUE(class_id, client_email)
    );
    """
)


# Get the current IST time
IST = pytz.timezone("Asia/Kolkata")
now = datetime.now(IST)


# Sample classes to populate the database (10 days from now)
classes = [
    (
        "Yoga",
        (now + timedelta(days=10)).isoformat(),
        "Rahul",
        10,
    ),
    (
        "Zumba",
        (now + timedelta(days=10)).isoformat(),
        "Nidhi",
        10,
    ),
    (
        "HIIT",
        (now + timedelta(days=10)).isoformat(),
        "Mohit",
        10,
    ),
]

# Insert sample classes only if the table is currently empty
counts = cursor.execute("SELECT COUNT(*) FROM classes").fetchone()[0]
if counts == 0:
    cursor.executemany(
        """
        INSERT INTO classes (
            name, datetime, instructor, available_slots
            ) VALUES (?, ?, ?, ?)
        """,
        classes,
    )

# Commit changes and close cursor
connection.commit()
cursor.close()

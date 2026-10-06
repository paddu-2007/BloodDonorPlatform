import sqlite3

conn = sqlite3.connect("blood_donor.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE donors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    phone TEXT,
    email TEXT,
    city TEXT,
    availability TEXT,
    last_donation TEXT,
    donations_count INTEGER DEFAULT 0,
    response_rate INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    blood_group TEXT,
    units_required INTEGER,
    emergency_level TEXT,
    hospital_name TEXT,
    required_date TEXT,
    location TEXT,
    contact TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()

print("Database Created Successfully")

conn.close()
cursor.execute("""
CREATE TABLE IF NOT EXISTS donations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER,
    hospital_name TEXT,
    donation_date TEXT,
    blood_units INTEGER
)
""")
import sqlite3

conn = sqlite3.connect("complaints.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    account TEXT,
    complaint TEXT,
    department TEXT,
    priority TEXT,
    status TEXT
)
""")

conn.commit()

# -------------------------
# INSERT
# -------------------------
def insert_complaint(name, email, account, complaint, dept, priority):
    cursor.execute("""
    INSERT INTO complaints (name, email, account, complaint, department, priority, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, account, complaint, dept, priority, "Pending"))
    conn.commit()

# -------------------------
# GET BY DEPARTMENT
# -------------------------
def get_by_department(dept):
    cursor.execute("SELECT * FROM complaints WHERE department=?", (dept,))
    return cursor.fetchall()

# -------------------------
# UPDATE STATUS
# -------------------------
def update_status(cid, status):
    cursor.execute("UPDATE complaints SET status=? WHERE id=?", (status, cid))
    conn.commit()

# -------------------------
# GET ALL (HISTORY)
# -------------------------
def get_all_complaints():
    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    return cursor.fetchall()
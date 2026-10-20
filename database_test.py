import sqlite3

connection = sqlite3.connect("evaluations.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    scenario TEXT,
    response TEXT
)
""")

cursor.execute("""
INSERT INTO evaluations (category, scenario, response)
VALUES (?, ?, ?)
""", (
    "Windows",
    "A Windows Server C: drive is 98% full.",
    "Check disk usage and identify the largest files or folders."
))

connection.commit()

cursor.execute("""
SELECT id, category, scenario, response
FROM evaluations
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

    
connection.close()

print("Database ready.")
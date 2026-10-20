import sqlite3

# Open a connection to the existing SQLite database.
connection = sqlite3.connect("evaluations.db")

# Create a cursor.
# The cursor sends SQL commands to the database.
cursor = connection.cursor()

# Add a new column called run_id.
# This will let us group several evaluation rows together
# as belonging to the same evaluator run.
cursor.execute("""
ALTER TABLE evaluations
ADD COLUMN run_id TEXT
""")

# Add a timestamp column.
# This will store when the evaluation was created.
cursor.execute("""
ALTER TABLE evaluations
ADD COLUMN created_at TEXT
""")

# Save the database structure changes.
connection.commit()

# Close the database connection.
connection.close()

print("Run tracking columns added.")
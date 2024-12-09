import os, sqlite3

database_root = os.path.dirname(os.path.dirname(__file__))
study_card_db_path = os.path.join(database_root, "study_card.db")

# Ensure StudyCard DB exists
if not os.path.exists(study_card_db_path):
    open(study_card_db_path, 'w').close()

conn = sqlite3.connect(study_card_db_path)
cursor = conn.cursor()

# Create the Config table to store single-user data
cursor.execute("""
CREATE TABLE IF NOT EXISTS Config (
    id INTEGER PRIMARY KEY,
    daily_streak INTEGER DEFAULT 0,
    last_login DATE,
    best_streak INTEGER DEFAULT 0
);
""")

# Insert default values for the Config table if it's empty
cursor.execute("""
INSERT OR IGNORE INTO Config (id, daily_streak, last_login, best_streak)
VALUES (1, 0, NULL, 0);
""")

# Create the StudyCards table
cursor.execute("""
CREATE TABLE IF NOT EXISTS StudyCards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INTEGER NOT NULL,
    reversed BOOLEAN DEFAULT FALSE,
    last_studied DATE,
    interval INTEGER DEFAULT 1,
    ease_factor REAL DEFAULT 2.5,
    review_count INTEGER DEFAULT 0,
    due_date DATE,
    last_quality INTEGER DEFAULT NULL
);
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_due_date ON StudyCards(due_date);
""")

# Commit and close
conn.commit()
conn.close()
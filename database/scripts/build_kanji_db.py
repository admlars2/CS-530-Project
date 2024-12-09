import pandas as pd
import os, sqlite3
from parse_xml import parse_kanjivg_xml

# Paths
database_root = os.path.dirname(os.path.dirname(__file__))
kanjivg_folder = os.path.join(database_root, "kanjivg")
word_list_path = os.path.join(database_root, "data", "top_3000_words.csv")
kanjivg_xml = os.path.join(database_root, "data", "kanjivg.xml")
kanji_database_path = os.path.join(database_root, "kanji.db")

# Ensure Kanji DB exists
if not os.path.exists(kanji_database_path):
    open(kanji_database_path, 'w').close()

# Connect to SQLite
conn = sqlite3.connect(kanji_database_path)
cursor = conn.cursor()

# Main Words Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    reading TEXT,
    translations TEXT,
    frequency INTEGER,
    svgs TEXT
);
""")

# Virtual Table for Translations
cursor.execute("""
CREATE VIRTUAL TABLE IF NOT EXISTS fts_translations
USING fts5(word, reading, translations);
""")

conn.commit()

# Load Data
word_df = pd.read_csv(word_list_path)
kanji_to_svg = parse_kanjivg_xml(kanjivg_xml)

# Populate Words Table and Virtual FTS Table
for _, row in word_df.iterrows():
    frequency = row["#"]
    word = row["japanese"]
    reading = row["pronounciation"]
    translations = row["translation"]

    # Process associated SVGs
    svgs = []
    for char in word:
        if char in kanji_to_svg:
            svgs.append(kanji_to_svg[char])
    svgs_str = ",".join(svgs)

    # Insert into Words table
    cursor.execute("""
    INSERT INTO Words (word, reading, translations, frequency, svgs)
    VALUES (?, ?, ?, ?, ?);
    """, (word, reading, translations, frequency, svgs_str))

    # Insert into FTS Translations table
    cursor.execute("""
    INSERT INTO fts_translations (word, reading, translations)
    VALUES (?, ?, ?);
    """, (word, reading, translations))

conn.commit()
conn.close()
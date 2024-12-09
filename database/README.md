# Kanji and Study Card Database Setup Guide

---

## Prerequisites

Ensure you have the following tools installed:

- Python 3.x
- SQLite
- Required Python libraries (Use Poetry)

---

## Steps to Build the Kanji and Study Card Databases

### 1. **Download Required Files**

#### a. **Top 3000 Words**

Download the list of the top 3000 Japanese words:

- **Link**: [Top 3000 Words Google Sheet](https://docs.google.com/spreadsheets/d/1cT16lcMnSoWW_VNO8DgPMKhPkXVj41ow7RZ0kuZQ4Jk/edit?gid=189116820#gid=189116820)
- Save it as `top_3000_words.csv` in the `data` folder.

#### b. **KanjiVG SVGs and XML**

Download the KanjiVG files:

1. Visit the [KanjiVG GitHub Releases](https://github.com/KanjiVG/kanjivg/releases).
2. Download the `kanjivg-(version)-main.zip`.
3. Extract the contents:
   - Place the SVG files into a folder named `kanjivg_all`.
   - Place the `kanjivg.xml` file into the `data` folder.

---

### 2. **Prepare the Data**
First change directory from the project root to the database folder.

```bash
cd database
```

#### a. **Format the Word List**

Run the `format_data.py` script to format the word list correctly:

```bash
py scripts/format_data.py
```

#### b. **Filter KanjiVG SVGs**

Run the `filter_kanjivg.py` script to process and filter the SVG files:

```bash
py scripts/filter_kanjivg.py
```

- This script will generate a new folder `kanjivg` containing the filtered SVGs.
- Once completed, you can delete the `kanjivg_all` folder.

#### c. **Optional: Convert Pronunciations**

If the pronunciations in the CSV file are in Romaji, you can convert them to Hiragana by running:

```bash
py scripts/convert_pronunciation.py
```

---

### 3. **Build the Kanji Database**

Run the `build_kanji_db.py` script to create the SQLite database:

```bash
py scripts/build_kanji_db.py
```

This script will:

1. Parse the formatted `top_3000_words.csv`.
2. Parse the `kanjivg.xml` file to map characters to their SVG files.
3. Create a database (`kanji.db`) with the following structure:
   - **Words Table**: Contains words, readings, translations, and associated SVGs.
   - **FTS5 Virtual Table**: Enables full-text search for translations.

---

### 4. **Build the Study Card Database**

Run the `build_study_card_db.py` script to create the `study_card.db`:

```bash
py scripts/build_study_card_db.py
```

This script will:

1. Create two tables: `Config` and `StudyCards`.
2. Set up an index for optimized queries on the `due_date` column.

#### **StudyCards Table Structure**

| Column          | Type      | Description                                      |
|------------------|-----------|--------------------------------------------------|
| `id`            | INTEGER   | Primary key for the study card.                  |
| `card_id`       | INTEGER   | References the `Words.id` in `kanji.db`.         |
| `reversed`      | BOOLEAN   | Indicates if the card is reversed.               |
| `last_studied`  | DATE      | Date when the card was last studied.             |
| `interval`      | INTEGER   | Days until the next review.                      |
| `ease_factor`   | REAL      | Adjusts card difficulty for spaced repetition.   |
| `review_count`  | INTEGER   | Number of times the card has been reviewed.      |
| `due_date`      | DATE      | When the card is due for review.                 |
| `last_quality`  | INTEGER   | Quality score of the last review (1–4).          |

#### **Config Table Structure**

| Column          | Type      | Description                                      |
|------------------|-----------|--------------------------------------------------|
| `id`            | INTEGER   | Always `1`, as the database is single-user.      |
| `daily_streak`  | INTEGER   | Tracks the user's current daily streak.          |
| `last_login`    | DATE      | Date of the last login.                          |
| `best_streak`   | INTEGER   | The best daily streak achieved by the user.      |

---

### 5. **Folder Structure**

After completing the steps, your folder should look like this:

```
project_root/
│
├── database/
│   │
│   ├── data/
│   │   ├── top_3000_words.csv
│   │   ├── romaji_map.json
│   │   └── kanjivg.xml
│   │
│   ├── kanjivg/ # Folder with filtered SVGs
│   │
│   ├── scripts/
│   │   │
│   │   ├── build_kanji_db.py
│   │   ├── build_study_card_db.py
│   │   ├── convert_pronunciation.py
│   │   ├── filter_kanjivg.py
│   │   ├── format_data.py
│   │   └── parse_xml.py
│   │   
│   ├── kanji.db        # Generated SQLite database for kanji data
│   ├── study_card.db   # Generated SQLite database for study cards
│   └── README.md       # This file
│      
└── ... # Rest of application
```

---

## Features of the Study Card Database

1. **Spaced Repetition Support**:
   - Implements a modified SuperMemo algorithm with 4 quality levels.
   - Tracks `ease_factor`, `interval`, and `last_quality` for effective learning.

2. **Efficient Card Management**:
   - Indexed `due_date` column for optimized lookups of due cards.

3. **User Progress Tracking**:
   - The `Config` table tracks daily streaks, login dates, and best streaks.
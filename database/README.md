# Kanji Database Setup Guide
---
## Prerequisites
Ensure you have the following tools installed:
- Python 3.x
- SQLite
- Required Python libraries (Use Poetry)
---

## Steps to Build the Kanji Database

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

#### a. **Format the Word List**
Run the `format_data.py` script to format the word list correctly:
```bash
py format_data.py
```

#### b. **Filter KanjiVG SVGs**
Run the `filter_kanjivg.py` script to process and filter the SVG files:
```bash
py filter_kanjivg.py
```
- This script will generate a new folder `kanjivg` containing the filtered SVGs.
- Once completed, you can delete the `kanjivg_all` folder.

#### c. **Optional: Convert Pronunciations**
If the pronunciations in the CSV file are in Romaji, you can convert them to Hiragana by running:
```bash
py convert_pronunciation.py
```

---

### 3. **Build the Kanji Database**
Run the `build_kanji_db.py` script to create the SQLite database:
```bash
py build_kanji_db.py
```
This script will:
1. Parse the formatted `top_3000_words.csv`.
2. Parse the `kanjivg.xml` file to map characters to their SVG files.
3. Create a database (`kanji.db`) with the following structure:
   - **Words Table**: Contains words, readings, translations, and associated SVGs.
   - **FTS5 Virtual Table**: Enables full-text search for translations.

---

## Folder Structure

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
│   ├── kanjivg/ # Folder with filtered SVGS
│   │
│   ├── scrips/ # Folder with filtered SVGS
│   │   │
│   │   ├── build_kanji_db.py
│   │   ├── convert_pronunciation.py
│   │   ├── filter_kanjivg.py
│   │   ├── format_data.py
│   │   └── parse_xml.py
│   │   
│   ├── kanji.db  # Generated SQLite database
│   └── README.md # This file
│      
└── ... # Rest of application
```

---

## Features of the Database

1. **Efficient Lookups**:
   - Indexed on `reading` (pronunciation) for fast queries.
   - Full-text search on `translations` using FTS5.

2. **Rich Data**:
   - Stores word frequency, readings, translations, and associated SVG paths.
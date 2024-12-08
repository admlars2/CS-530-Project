import pandas as pd
import os, shutil
from parse_xml import parse_kanjivg_xml

# Define paths
database_root = os.path.dirname(os.path.dirname(__file__))
kanji_all_folder = os.path.join(database_root, "kanjivg_all")  # Folder with all SVG files
kanji_filtered_folder = os.path.join(database_root, "kanjivg")  # Folder for filtered SVGs
word_list_path = os.path.join(database_root, "data", "top_3000_words.csv")  # CSV with word list
kanjivg_xml = os.path.join(database_root, "data", "kanjivg.xml")  # XML file with kanji mapping

# Load word list
word_df = pd.read_csv(word_list_path)
word_list = word_df["japanese"].to_list()

# Ensure filtered folder exists
os.makedirs(kanji_filtered_folder, exist_ok=True)

# Get kanji-to-SVG mapping
kanji_to_svg = parse_kanjivg_xml(kanjivg_xml)

count = 0

# Filter and copy relevant SVGs
for word in word_list:
    for char in word:
        if char in kanji_to_svg:
            svg_filename = kanji_to_svg[char]
            source_path = os.path.join(kanji_all_folder, svg_filename)
            dest_path = os.path.join(kanji_filtered_folder, svg_filename)

            # Copy the SVG file if it exists
            if os.path.exists(source_path):
                if not os.path.exists(dest_path):  # Avoid redundant copies
                    try:
                        shutil.copy(source_path, dest_path)
                        count += 1
                    except Exception as e:
                        print(f"Failed to copy {source_path} to {dest_path}: {e}")

            else:
                print(f"SVG for {char} ({svg_filename}) not found in {kanji_all_folder}.")

print(f"Successfully copied {count} files.")
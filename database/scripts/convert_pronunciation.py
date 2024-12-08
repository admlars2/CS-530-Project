import pandas as pd
import os, json

# Database root
database_root = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(database_root, "data", "top_3000_words.csv")

romaji_path = os.path.join(database_root, "data", "romaji_map.json")
with open(romaji_path, "r", encoding="utf-8") as file:
    romaji_map =  json.load(file)

def romaji_to_hiragana(romaji):
    result = ""
    temp = ""
    for char in romaji:
        temp += char
        if temp in romaji_map:
            result += romaji_map[temp]
            temp = ""
    return result

# Read the csv file
df = pd.read_csv(csv_path)

# Clean the "pronounciation" column
df["pronounciation"] = df["pronounciation"].fillna("").astype(str)

# Apply coversion
df["pronounciation"] = df["pronounciation"].apply(lambda romaji: romaji_to_hiragana(romaji))

df.to_csv(csv_path, index=False)
import pandas as pd
import os

# Database root
database_root = os.path.dirname(os.path.dirname(__file__))

# Read the csv file
df = pd.read_csv(os.path.join(database_root, "data", "3000 common JP words - All.csv"), dtype={"#": int})

# Filter the columns
filtered_df = df[['#', 'japanese', 'pronounciation', 'translation']]

# Save to a new CSV file or display
filtered_df.to_csv(os.path.join(database_root, "data", "top_3000_words.csv"), index=False)
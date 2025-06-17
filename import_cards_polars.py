import polars as pl
import glob
import json
import sqlite3

# Path to your JSON files
json_folder = "data/OP01-EB02"
json_files = glob.glob(f"{json_folder}/cards_*.json")

# Collect all card dicts
all_cards = []
for file in json_files:
    with open(file, "r") as f:
        data = json.load(f)
        if isinstance(data, dict):
            cards = list(data.values())
        elif isinstance(data, list):
            cards = data
        else:
            continue
        all_cards.extend(cards)

# Create a Polars DataFrame
if all_cards:
    df = pl.DataFrame(all_cards)
    print(df.head())
    # Optionally, write to SQLite using pandas
    # import pandas as pd
    # conn = sqlite3.connect("cards.db")
    # df.to_pandas().to_sql("cards", conn, if_exists="replace", index=False)
    # conn.close()
else:
    print("No card data found.") 
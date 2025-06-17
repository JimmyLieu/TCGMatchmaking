import polars as pl
import glob
import json
import pandas as pd
from sqlalchemy import create_engine
import numpy as np


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


if all_cards:
    df = pl.DataFrame(all_cards)
    print(df.head())

    pdf = df.to_pandas()
    for col in pdf.columns:
        if pdf[col].apply(type).isin([np.ndarray]).any():
            pdf[col] = pdf[col].apply(lambda x: ", ".join(x) if isinstance(x, np.ndarray) else x)

    engine = create_engine("postgresql+psycopg2://jimmylieu@localhost:5432/optcg")

    pdf.to_sql("cards", engine, if_exists="replace", index=False)
    print("Saved cards to PostgreSQL (table: cards)")
else:
    print("No card data found.")
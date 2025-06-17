import pandas as pd
from sqlalchemy import create_engine

# Load your decklist CSV
decklist_df = pd.read_csv("all_decklists.csv")

# Connect to your PostgreSQL database
engine = create_engine("postgresql+psycopg2://jimmylieu@localhost:5432/optcg")

# Read the cards table from PostgreSQL
cards_df = pd.read_sql("SELECT * FROM cards", engine)

# Merge decklist with card details
merged = decklist_df.merge(cards_df, left_on="Card Code", right_on="id", how="left")

# Show the first few rows
print(merged.head())

# Optionally, save to a new CSV
merged.to_csv("enriched_decklists.csv", index=False) 
from sqlalchemy import create_engine
import pandas as pd

DB_URL = "sqlite:///data/transactions.db"
engine = create_engine(DB_URL)

def save_transactions_to_db(df: pd.DataFrame) -> None:
    with engine.begin() as conn:
        df.to_sql("transactions", conn, if_exists="append", index=False)


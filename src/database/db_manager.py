from sqlalchemy import create_engine, text, inspect
import pandas as pd

DB_URL = "sqlite:///data/finance.db"
engine = create_engine(DB_URL)

def table_exists(table_name):
    inspector = inspect(engine)
    return inspector.has_table(table_name)

def save_transactions_to_db(df: pd.DataFrame) -> None:
    with engine.begin() as conn:
        df.to_sql("transactions", conn, if_exists="append", index=False)



def save_budget_to_db(year: int, inc_data: list, exp_data: list, sav_data: list) -> None:
    # 1. Convert lists of dicts to DataFrames and add their Section
    df_inc = pd.DataFrame(inc_data).assign(section="Inkomst")
    df_exp = pd.DataFrame(exp_data).assign(section="Utgift")
    df_sav = pd.DataFrame(sav_data).assign(section="Sparande")
    
    # 2. Combine all three
    df_all = pd.concat([df_inc, df_exp, df_sav], ignore_index=True)
    
    if df_all.empty:
        return

    # 3. "Melt" the data: Turn month columns (jan, feb...) into rows
    months = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
    
    df_long = df_all.melt(
        id_vars=["Category", "section"], 
        value_vars=months,
        var_name="month_name", 
        value_name="amount"
    )
    
    # Add the year column
    df_long["year"] = year
    # Ensure amount is numeric (cleaning any empty strings or None)
    df_long["amount"] = pd.to_numeric(df_long["amount"]).fillna(0)

    # 4. Save to DB using your connection logic
    with engine.begin() as conn:
        # Remove old budget for this year first so we don't double up
        if table_exists("budget"): # Feels like a quick fix...
            conn.execute(text("DELETE FROM budget WHERE year = :year"), {"year": year})
        
        # Save the new long-format data
        df_long.to_sql("budget", conn, if_exists="append", index=False)

def load_budget_from_db(year: int):
    if table_exists("budget"):
        query = f"SELECT * FROM budget WHERE year = {year}"
        df = pd.read_sql(query, engine)
    else:
        df = pd.DataFrame()
    # If the database is empty for this year, return empty lists
    if df.empty:
        return [], [], []

    # Pivot the data: 
    # Index: Category & section (these stay as rows)
    # Columns: month_name (these become our jan, feb, mar... columns)
    # Values: amount
    df_wide = df.pivot(
        index=["Category", "section"], 
        columns="month_name", 
        values="amount"
    ).reset_index()
    
    # Ensure all 12 months exist in the dataframe even if some are missing in DB
    months = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
    for m in months:
        if m not in df_wide.columns:
            df_wide[m] = 0
            
    # Split the DataFrame back into three separate lists of dictionaries
    inc = df_wide[df_wide["section"] == "Inkomst"].to_dict("records")
    exp = df_wide[df_wide["section"] == "Utgift"].to_dict("records")
    sav = df_wide[df_wide["section"] == "Sparande"].to_dict("records")
    
    return inc, exp, sav
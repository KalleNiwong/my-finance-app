import pandas as pd
from database.db_manager import save_transactions_to_db
import dash_mantine_components as dmc
import base64
import io


def parse_xlsx(contents, filename) -> pd.DataFrame:

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
        
    if filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(decoded), header=8, engine="calamine")
    
    # Clean up: Remove completely empty rows or columns often found in bank exports
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # Standardize column names (lowercase and no spaces) before DB save
    df.columns = [str(c).lower().strip() for c in df.columns]

    date_col = "transaktionsdatum"
    desc_col = "text"
    val_col = "belopp"

    df_clean = df[[date_col, desc_col, val_col]]
    df_clean["belopp"] = df_clean["belopp"].round(0).astype(int)

    return df_clean 
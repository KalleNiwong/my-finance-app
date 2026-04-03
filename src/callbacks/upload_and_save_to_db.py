import base64
import io
import pandas as pd
from dash import Output, Input, State, callback
from database.db_manager import save_transactions_to_db
import dash_mantine_components as dmc
from utils.parser import parse_xlsx

@callback(
    Output("upload-display-grid", "rowData"),
    Output("upload-status", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def handle_upload(contents, filename):
    if contents is None:
        return ""

    try:
        df = parse_xlsx(contents, filename)

        # save_transactions_to_db(df)
        
        return df.to_dict("records"), f"Reviewing {filename}..."
        
    except Exception as e:
        # Returning a red text for errors
        return pd.DataFrame().to_dict("records"), dmc.Text(f"❌ Error: {str(e)}")
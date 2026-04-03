from dash import Dash
import dash_mantine_components as dmc
from callbacks import upload_and_save_to_db
from layout import create_layout

app = Dash(__name__)

app.layout = create_layout()

if __name__ == "__main__":
    app.run(debug=True)
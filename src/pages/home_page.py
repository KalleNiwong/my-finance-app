import dash
import dash_mantine_components as dmc
from dash import html

# Register this page with a specific path
dash.register_page(__name__, path='/', name="Startsida")

layout = html.Div([
    dmc.Container(
        [
            dmc.Title("Startsida", order=2, mb="xl"),
            dmc.Text("WIP...")
        ],
        size="md",
        pt="xl"
    )
])
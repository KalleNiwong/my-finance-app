import dash
import dash_mantine_components as dmc
from dash import html

# Register this page with a specific path
dash.register_page(__name__, path='/dashboard', name="Dashboard")

layout = html.Div([
    dmc.Container(
        [
            dmc.Title("Financial Dashboard", order=2, mb="xl"),
            dmc.Text("Your analytics and charts will go here.")
        ],
        size="md",
        pt="xl"
    )
])
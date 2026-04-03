import dash
import dash_mantine_components as dmc
from dash import dcc, html
from components.upload import create_upload_component, generate_upload_display_table

# Register this as the home page (path='/')
dash.register_page(__name__, path='/upload_page', name="Upload Data")

# Define the layout variable that Dash Pages expects
layout = html.Div([
    dcc.Store(id="staged-data-store"),
    dmc.Container(
        [
            dmc.Title("Upload Center", order=2, mb="xl"),
            create_upload_component(), 
            generate_upload_display_table(),
            dmc.Box(id="grid-container", mt="xl")
        ], 
        size="md", 
        pt="xl"
    )
])
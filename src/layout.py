import dash_mantine_components as dmc
from components.upload import create_upload_component, generate_upload_display_table
from dash import dcc

dcc.Store(id="staged-data-store")

def create_layout() -> dmc.MantineProvider:
    return dmc.MantineProvider(
    children=[
        dmc.Container([
            dmc.Title("FinanceOS", order=1, mb="xl"),
            create_upload_component(), 
            generate_upload_display_table(),
            dmc.Box(id="grid-container", mt="xl")
        ], size="md", pt="xl")
    ]
)
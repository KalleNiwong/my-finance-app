import dash
from dash import Dash
import dash_mantine_components as dmc
from components.sidebar_buttons import create_sidebar_button

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,700;1,400&display=swap"
]

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

from callbacks import cb_budget

sidebar = dmc.AppShellNavbar(
    dmc.Stack(
        [
            dmc.Title("My Finance App", order=3, c="blue", mb="xl"), 
            create_sidebar_button("Startsida", "material-symbols:home-outline-rounded", "/"),
            create_sidebar_button("Budget", "material-symbols:calculate-outline-rounded", "/budget"),
            create_sidebar_button("Transaktioner", "material-symbols:list-rounded", "/transactions"),
            create_sidebar_button("Dashboard", "material-symbols:dashboard-outline-rounded", "/dashboard"),
            
        ],
        gap="sm",
    ),
    p="md",
)

app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "headings": {"fontFamily": "'Inter', sans-serif"},
    },
    children=[
        dmc.AppShell(
            [sidebar, dmc.AppShellMain(dash.page_container)],
            navbar={"width": 250, "breakpoint": "sm"}, 
            padding="md"
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
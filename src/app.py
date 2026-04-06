import dash
from dash import Dash
import dash_mantine_components as dmc
from components.sidebar_buttons import create_sidebar_button

app = Dash(__name__, use_pages=True)

sidebar = dmc.AppShellNavbar(
    dmc.Stack(
        [
            dmc.Title("My Finance App", order=3, c="blue", mb="xl"), 
            create_sidebar_button("Startsida", "material-symbols:home-outline-rounded", "/"),
            create_sidebar_button("Transaktioner", "material-symbols:list-rounded", "/transactions"),
            create_sidebar_button("Dashboard", "material-symbols:dashboard-outline-rounded", "/dashboard"),
            create_sidebar_button("Budget", "material-symbols:calculate-outline-rounded", "/budget")
        ],
        gap="sm",
    ),
    p="md",
)

app.layout = dmc.MantineProvider(
    dmc.AppShell(
        [sidebar, dmc.AppShellMain(dash.page_container)],
        navbar={"width": 250, "breakpoint": "sm"}, 
        padding="md"
    )
)

if __name__ == "__main__":
    app.run(debug=True)
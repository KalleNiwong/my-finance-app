import dash
from dash import Dash, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify # Import the icon component

app = Dash(__name__, use_pages=True)

# Helper function to keep code clean
def get_icon(icon):
    return DashIconify(icon=icon, width=20)

sidebar = dmc.AppShellNavbar(
    dmc.Stack(
        [
            dmc.Title("My Finance App", order=3, c="blue", mb="xl"), 
            
            dcc.Link(
                dmc.Button(
                    "Startsida",
                    leftSection=get_icon("material-symbols:home-outline-rounded"), # can change to "-light"
                    variant="subtle", 
                    fullWidth=True, 
                    justify="left"
                ), 
                href="/", 
                style={"textDecoration": "none"}
            ),
            dcc.Link(
                dmc.Button(
                    "Transaktioner",  # TODO: this handles both new transaktions and looking at all
                    leftSection=get_icon("material-symbols:list-rounded"), # can change to "-light"
                    variant="subtle", 
                    fullWidth=True, 
                    justify="left"
                ), 
                href="/transactions", 
                style={"textDecoration": "none"}
            ),
            dcc.Link(
                dmc.Button(
                    "Dashboard", 
                    leftSection=get_icon("material-symbols:dashboard-outline-rounded"), # can change to "-light"
                    variant="subtle", 
                    fullWidth=True, 
                    justify="left"
                ), 
                href="/dashboard", 
                style={"textDecoration": "none"}
            ),
            dcc.Link(
                dmc.Button(
                    "Budget", 
                    leftSection=get_icon("material-symbols:dashboard-outline-rounded"), # can change to "-light"
                    variant="subtle", 
                    fullWidth=True, 
                    justify="left"
                ), 
                href="/budget", 
                style={"textDecoration": "none"}
            ),
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
from dash import dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def get_icon(icon):
    return DashIconify(icon=icon, width=20)


def create_sidebar_button(name: str, icon: str, page: str) -> dcc.Link:
    return dcc.Link(
                dmc.Button(
                    name,
                    leftSection=get_icon(icon), #
                    variant="subtle", 
                    fullWidth=True, 
                    justify="left"
                ), 
                href=page, 
                style={"textDecoration": "none"}
            )
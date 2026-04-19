import dash
import dash_mantine_components as dmc
from dash import html
from components.budget_grids import create_grid
dash.register_page(__name__, path='/budget', name="Budget Planner")

# --- UI COMPONENTS ---
header = dmc.Group(
    [
        # Left side: Title and Italic Subtitle
        dmc.Stack(
            [
                dmc.Title("Budget", order=3),
                dmc.Text('"Do not save what is left after spending; instead spend what is left after saving." - Warren Buffet', size="sm", c="dimmed"),
            ],
            gap=0, # Removes the vertical space between title and subtitle
        ),
        
        # Right side: Button and Select with Label
        dmc.Group(
            [
                dmc.Button(
                    "Lägg till Kategori", 
                    id="open-modal-btn", 
                    variant="light", 
                    size="sm"
                ),
                dmc.Select(
                    id="year-select",
                    label="Välj År",
                    data=["2024", "2025", "2026"],
                    value="2026",
                    w=100, 
                    size="sm",
                ),
            ],
            align="flex-end", # Aligns the button with the bottom of the select input
        ),
    ],
    justify="space-between",
    mb="md",
)

modal = dmc.Modal(
    title="Lägg till ny kategori",
    id="add-modal",
    zIndex=10000,
    children=[
        dmc.RadioGroup(
            label="Typ",
            id="modal-type",
            children=dmc.Group(
                [dmc.Radio(value=i.lower(), label=i) for i in ["Inkomst", "Utgift", "Sparande"]], #my=10
            ),
        ),
        dmc.TextInput(id="modal-category", label="Kategori", placeholder="T.ex. Livsmedel", mb="md"),
        dmc.Button("Spara", id="modal-save-btn", fullWidth=True)
    ]
)

# Add this to your layout, perhaps in a Sticky footer or below the last grid
save_controls = dmc.Stack([
    dmc.Button("Spara Ändringar", id="save-budget-btn", color="teal", variant="filled"),
    html.Div(id="save-notification")
], justify="flex-end", mt="xl", style={"width": 150})

# Add save_controls to your layout Container...

# --- LAYOUT ---
layout = dmc.Container([
    modal,
    header,
    
    # We use smaller margins (mb="sm") to compress the view
    dmc.Stack([
    create_grid("grid-status", "Budgetstatus", is_status=True),
    create_grid("grid-inkomst", "Inkomst", accent_color="#8ED973"),
    create_grid("grid-utgift", "Utgift", accent_color="#F1A983"),
    create_grid("grid-sparande","Sparande", accent_color="#61CBF3")
    ], gap="m"),
    save_controls
], size="xl", pt="md")

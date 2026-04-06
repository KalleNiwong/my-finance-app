import dash
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash import html, Input, Output, State, callback, clientside_callback, ClientsideFunction, no_update

dash.register_page(__name__, path='/budget', name="Budget Planner")

months = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]

# --- GRID COLUMNS ---
# Removed 'Section' since the tables are separated now.
columnDefs = [{"field": "Category", "pinned": "left", "width": 150}]
for month in months:
    columnDefs.append({
        "field": month,
        "editable": True,
        "type": "numericColumn",
        "width": 80, # Made slightly narrower to fit smaller screens better
        "valueFormatter": {"function": "d3.format(',.0f')(params.value)"}
    })

def create_budget_grid(grid_id):
    return dag.AgGrid(
        id=grid_id,
        columnDefs=columnDefs,
        rowData=[], 
        # Move it INSIDE dashGridOptions
        dashGridOptions={
            "rowSelection": "single", 
            "stopEditingWhenCellsLoseFocus": True,
            "domLayout": "autoHeight",
            "pinnedBottomRowData": [{"Category": "Total"}] ,
            # "rowHeight": 30,      # Standard is ~45. 30 is very "Excel-slim"
            # "headerHeight": 32,   # Shrinks the header row height
        },
        defaultColDef={"resizable": True, "sortable": False, "editable": True, "suppressMovableColumns": True},
        className="ag-theme-balham",
        getRowStyle={
            "styleConditions": [
                {"condition": "params.node.rowPinned === 'bottom'", "style": {"fontWeight": "bold", "backgroundColor": "#f8f9fa", "borderTop": "1px solid #dee2e6"}}
            ]
        }
    )

# --- UI COMPONENTS ---
header = dmc.Group([
    dmc.Title("Zero-Based Budget", order=3),
    dmc.Group([
        dmc.Button("Lägg till Kategori", id="open-modal-btn", variant="light", size="sm"),
        dmc.Select(id="year-select", data=["2024", "2025", "2026"], value="2026", w=100, size="sm")
    ])
], justify="space-between", mb="md")

summary_bar = dmc.Paper(
    withBorder=True, p="xs", radius="md", mb="md", shadow="sm",
    children=[
        dmc.Group([
            dmc.Text("Ska allokeras:", fw=700, size="sm", c="dimmed"),
            html.Div(id="summary-status-container", style={"display": "flex", "gap": "8px", "flexWrap": "wrap"})
        ])
    ]
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

# --- LAYOUT ---
layout = dmc.Container([
    modal,
    header,
    summary_bar,
    
    # We use smaller margins (mb="sm") to compress the view
    dmc.Text("Inkomst", fw=600, c="teal", size="sm", mb=4),
    create_budget_grid("grid-inkomst"),
    
    dmc.Text("Utgift", fw=600, c="red", size="sm", mt="sm", mb=4),
    create_budget_grid("grid-utgift"),
    
    dmc.Text("Sparande", fw=600, c="blue", size="sm", mt="sm", mb=4),
    create_budget_grid("grid-sparande"),

], size="xl", pt="md") # pt="md" instead of "xl" to move it up slightly


# --- CALLBACK 1: MODAL OPEN / CLOSE & ADD ROW ---
@callback(
    Output("add-modal", "opened"),
    Output("grid-inkomst", "rowData"),
    Output("grid-utgift", "rowData"),
    Output("grid-sparande", "rowData"),
    Output("modal-category", "value"), # Reset input after save
    Input("open-modal-btn", "n_clicks"),
    Input("modal-save-btn", "n_clicks"),
    State("modal-type", "value"),
    State("modal-category", "value"),
    State("grid-inkomst", "rowData"),
    State("grid-utgift", "rowData"),
    State("grid-sparande", "rowData"),
    prevent_initial_call=True
)
def handle_modal_and_add_row(open_clicks, save_clicks, row_type, category_name, inc_data, exp_data, sav_data):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Open the modal
    if triggered_id == "open-modal-btn":
        return True, no_update, no_update, no_update, no_update

    # Save the new row to the correct table and close modal
    if triggered_id == "modal-save-btn" and category_name:
        new_row = {"Category": category_name, **{m: 0 for m in months}}
        
        # Default fallbacks if data is None on first load
        inc_data = inc_data or []
        exp_data = exp_data or []
        sav_data = sav_data or []

        if row_type == "inkomst":
            return False, inc_data + [new_row], no_update, no_update, ""
        elif row_type == "utgift":
            return False, no_update, exp_data + [new_row], no_update, ""
        elif row_type == "sparande":
            return False, no_update, no_update, sav_data + [new_row], ""

    return False, no_update, no_update, no_update, no_update


# --- CALLBACK 2: CLIENTSIDE MATH (Fixed Outputs) ---
clientside_callback(
    ClientsideFunction(namespace="budget", function_name="calculateAll"),
    # Output("summary-status-container", "dangerouslySetInnerHTML"),
    Output("grid-inkomst", "dashGridOptions"),
    Output("grid-utgift", "dashGridOptions"),
    Output("grid-sparande", "dashGridOptions"),
    Input("grid-inkomst", "virtualRowData"),
    Input("grid-utgift", "virtualRowData"),
    Input("grid-sparande", "virtualRowData"),
    Input("grid-inkomst", "cellValueChanged"),
    Input("grid-utgift", "cellValueChanged"),
    Input("grid-sparande", "cellValueChanged"),
    State("grid-inkomst", "dashGridOptions"),
    State("grid-utgift", "dashGridOptions"),
    State("grid-sparande", "dashGridOptions"),
)
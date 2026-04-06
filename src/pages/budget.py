import dash
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash import html, Input, Output, State, callback, clientside_callback, ClientsideFunction, no_update
from database.db_manager import save_budget_to_db, load_budget_from_db
dash.register_page(__name__, path='/budget', name="Budget Planner")

months = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]

def create_budget_grid(grid_id, header_name, accent_color="#228be6"):
    # 1. Generate columns locally so we can customize the first header
    grid_cols = [
        {
            "headerName": header_name,  # This is the visible title (Inkomst, etc.)
            "field": "Category",        # Keep this as 'Category' for your DB/callbacks
            "pinned": "left", 
            "width": 200,               # Slimmed down from 200
            "cellStyle": {"fontWeight": "bold"} 
        }
    ]
    
    for month in months:
        grid_cols.append({
            "field": month,
            "editable": True,
            "type": "numericColumn",
            "width": 75, # Slimmed down to fit 12 months easily
            "valueFormatter": {
                "function": "params.value != null ? d3.format(',.0f')(params.value).replace(/,/g, ' ') : ''"
            }
        })

    return dag.AgGrid(
        id=grid_id,
        columnDefs=grid_cols,
        rowData=[], 
        dashGridOptions={
            "rowSelection": "single", 
            "stopEditingWhenCellsLoseFocus": True,
            "domLayout": "autoHeight",
            "pinnedBottomRowData": [{"Category": "Total"}],
            "rowHeight": 24,
            "headerHeight": 24,
        },
        defaultColDef={
            "resizable": True, 
            "sortable": False, 
            "editable": True, 
            "suppressMovable": True,
            "cellStyle": {"display": "flex", "alignItems": "center"}
        },
        style={
            "--ag-active-color": accent_color,
            "--ag-header-background-color": f"{accent_color}90", # 40% opacity for better text contrast
            "--ag-background-color": f"{accent_color}10" # Very subtle tint for the grid body
        },
        className="ag-theme-balham",
        getRowStyle={
            "styleConditions": [
                {
                    "condition": "params.node.rowPinned === 'bottom'", 
                    "style": {
                        "fontWeight": "bold", 
                        "backgroundColor": "#f8f9fa", 
                        "borderTop": f"2px solid {accent_color}"
                    }
                }
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
    summary_bar,
    
    # We use smaller margins (mb="sm") to compress the view
    dmc.Stack([
        create_budget_grid("grid-inkomst", "Inkomst", "#8ED973"),
    
    create_budget_grid("grid-utgift", "Utgift" ,"#F1A983"),
    
    create_budget_grid("grid-sparande","Sparande", "#61CBF3")
    ], gap="m"),
    save_controls
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

@callback(
    Output("save-notification", "children"),
    Input("save-budget-btn", "n_clicks"),
    State("year-select", "value"),
    State("grid-inkomst", "rowData"),
    State("grid-utgift", "rowData"),
    State("grid-sparande", "rowData"),
    prevent_initial_call=True
)
def update_database(n_clicks, year, inc_data, exp_data, sav_data):
    try:
        # Call the helper function created in step 1
        save_budget_to_db(int(year), inc_data, exp_data, sav_data)
        # return dmc.Notification( #TODO: understand how dmc.Notifications work
        #     title="Sparat!",
        #     message=f"Budgeten för {year} har uppdaterats i databasen.",
        #     color="green",
        #     action="show"
        # )
        return "Sparat!"
    except Exception as e:
        print(e)
        return dmc.Notification(
            title="Ett fel uppstod",
            message=str(e),
            color="red",
            action="show"
        )
    
@callback(
    Output("grid-inkomst", "rowData", allow_duplicate=True),
    Output("grid-utgift", "rowData", allow_duplicate=True),
    Output("grid-sparande", "rowData", allow_duplicate=True),
    Input("year-select", "value"),
    # This is the magic string that fixes the error
    prevent_initial_call='initial_duplicate' 
)
def populate_grids_on_load(selected_year):
    if not selected_year:
        return [], [], []
        
    inc_data, exp_data, sav_data = load_budget_from_db(int(selected_year))
    
    return inc_data, exp_data, sav_data
import dash
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash import html, dcc
dash.register_page(__name__, path='/budget', name="Budget Planner")

months = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]

def create_budget_grid(grid_id, header_name, accent_color="#228be6"):
    # 1. Generate columns locally so we can customize the first header
    grid_cols = [
        {
            "headerName": header_name,  # This is the visible title (Inkomst, etc.)
            "field": "Category",        # Keep this as 'Category' for your DB/callbacks
            "pinned": "left", 
            "width": 200,            
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
                "function": "params.value != null ? d3.format(',.0f')(params.value).replace(/,/g, ' ') : ''" # to get the space number formatting e.g., "3 000" and "1 000 000" which I like
            }
        })


# --- ADD THIS NEW BLOCK ---
    # Create a JavaScript formula string that sums all 12 months dynamically.
    # It builds: params.data ? (Number(params.data.jan) || 0) + (Number(params.data.feb) || 0) ... : 0
    sum_logic = "params.data ? " + " + ".join([f"(Number(params.data.{m}) || 0)" for m in months]) + " : 0"

    grid_cols.append({
        "headerName": "Total",
        "field": "row_total", # This field name doesn't need to exist in your database
        "editable": False,    # Lock this column so users can't overwrite the math
        "pinned": "right",    # Pinning it to the right ensures it stays visible even on small screens
        "type": "numericColumn",
        "width": 90,
        "cellStyle": {
            "fontWeight": "bold", 
            "backgroundColor": f"{accent_color}15" # Give it a light tint to match your theme
        },
        "valueGetter": {"function": sum_logic},
        "valueFormatter": {
            "function": "params.value != null ? d3.format(',.0f')(params.value).replace(/,/g, ' ') : ''"
        }
    })
        
    return dag.AgGrid(
        id=grid_id,
        columnDefs=grid_cols,
        rowData=[], 
        columnSize="responsiveSizeToFit", # <- Is this the best solution for different screen types, I guess not...
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

def create_status_grid(grid_id):
    # Matches the exact column widths of your main grids
    status_cols = [
        {
            "headerName": "", 
            "field": "Category", 
            "pinned": "left", 
            "width": 200, 
            "cellStyle": {"fontWeight": "bold", "border": "none"}
        }
    ]
    
    for month in months:
        status_cols.append({
            "field": month,
            "width": 75,
            "type": "numericColumn",
            "cellStyle": {
                "styleConditions": [
                    {"condition": "params.value == 0", "style": {"backgroundColor": "#ebfbee", "color": "#2b8a3e"}},
                    {"condition": "params.value != 0", "style": {"backgroundColor": "#fff5f5", "color": "#c92a2a"}}
                ]
            },
            "valueFormatter": {"function": "params.value == 0 ? '✓' : d3.format(',.0f')(params.value).replace(/,/g, ' ')"}
        })

    # Add the Total column to match the others
    status_cols.append({
        "field": "row_total",
        "width": 90,
        "pinned": "right",
        "cellStyle": {
            "styleConditions": [
                {"condition": "params.value == 0", "style": {"backgroundColor": "#ebfbee", "color": "#2b8a3e", "fontWeight": "bold"}},
                {"condition": "params.value != 0", "style": {"backgroundColor": "#fff5f5", "color": "#c92a2a", "fontWeight": "bold"}}
            ]
        },
        "valueFormatter": {"function": "params.value == 0 ? '✓' : d3.format(',.0f')(params.value).replace(/,/g, ' ')"}
    })

    return dag.AgGrid(
        id=grid_id,
        columnDefs=status_cols,
        rowData=[{"Category": "Att allokera"}], # Initial dummy row
        columnSize="responsiveSizeToFit",
        dashGridOptions={
            "headerHeight": 24, 
            "rowHeight": 24,
            "domLayout": "autoHeight",
            "suppressNoRowsOverlay": True,
        },
        className="ag-theme-balham",
    )

# --- UI COMPONENTS ---
header = dmc.Group([
    dmc.Title("Budget", order=3),
    dmc.Group([
        dmc.Button("Lägg till Kategori", id="open-modal-btn", variant="light", size="sm"),
        dmc.Select(id="year-select", data=["2024", "2025", "2026"], value="2026", w=100, size="sm")
    ])
], justify="space-between", mb="md")


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
    create_status_grid("grid-status"),
    create_budget_grid("grid-inkomst", "Inkomst", "#8ED973"),
    create_budget_grid("grid-utgift", "Utgift" ,"#F1A983"),
    create_budget_grid("grid-sparande","Sparande", "#61CBF3")
    ], gap="m"),
    save_controls
], size="xl", pt="md")

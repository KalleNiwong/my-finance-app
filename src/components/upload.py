import dash_mantine_components as dmc
from dash import dcc, html
import dash_ag_grid as dag

def create_upload_component() -> dmc.Paper:
    upload_component = dmc.Paper(
        withBorder=True,
        p="md",
        children=[
            dcc.Upload(
                id="upload-data",
                children=html.Div([
                    dmc.Text("Drag and Drop or ", span=True),
                    dmc.Anchor("Select Excel/CSV File", href="#")
                ]),
                style={
                    "width": "100%", "height": "60px", "lineHeight": "60px",
                    "borderWidth": "1px", "borderStyle": "dashed",
                    "borderRadius": "5px", "textAlign": "center"
                },
                multiple=False
            ),
            dmc.Space(h=10),
            dmc.Text(id="upload-status", size="sm")
        ]
    )
    return upload_component



def generate_upload_display_table() -> dag.AgGrid:
    columnDefs = [
        {"field": "transaktionsdatum", "headerName": "Datum", "width": 120, "suppressSizeToFit": True},
        {"field": "text", "headerName": "Beskrivning", "editable": True, "flex": 2}, 
        {"field": "belopp", "headerName": "Belopp", "width": 100, "suppressSizeToFit": True},
        {
            "field": "typ", 
            "headerName": "Typ", 
            "editable": True,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"values": ["Inkomst", "Utgift", "Sparande"]},
            "width": 100,
            "suppressSizeToFit": True
        },
        {
            "field": "kategori", 
            "headerName": "Kategori", 
            "editable": True,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"values": ["Food", "Rent", "Salary", "Entertainment"]},
            "flex": 1 
        },
        {
            "field": "källa",
            "headerName": "Källa",
            "editable": False,
            "width": 100,
            "suppressSizeToFit": True
        },
        {
            "field": "från_konto", 
            "headerName": "Från Konto", 
            "editable": True,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"values": ["Checking", "Savings", "Credit Card"]},
            "width": 110,
            "suppressSizeToFit": True
        },
        {
            "field": "till_konto",
            "headerName": "Till Konto",
            "editable": True,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"values": ["Checking", "Savings", "Credit Card"]},
            "width": 110,
            "suppressSizeToFit": True
        },
    ]

    grid = dag.AgGrid(
        id="upload-display-grid",
        columnDefs=columnDefs,
        rowData=[],
        dashGridOptions={
            "rowSelection": {"mode": "multiRow"},
            "rowHeight": 45,
        },
        dangerously_allow_code=True # for badges
    )
    return grid
import dash_ag_grid as dag

MONTHS = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]

NUMERIC_FORMAT = {"function": "params.value != null ? d3.format(',.0f')(params.value).replace(/,/g, ' ') : ''"}

STATUS_FORMAT = {"function": "params.value == 0 ? '✓' : d3.format(',.0f')(params.value).replace(/,/g, ' ')"}

def _get_base_columns(header_name, is_status=False, accent_color="#228be6"):
    """Internal helper to build the column list to ensure consistent widths."""
    
    # Category Column (Pinned Left)
    cols = [{
        "headerName": header_name,
        "field": "Category",
        "pinned": "left",
        "width": 200,
        "cellStyle": {"fontWeight": "bold"}
    }]
    
    # Month Columns
    for m in MONTHS:
        col = {
            "field": m,
            "width": 75,
            "type": "numericColumn",
            "editable": not is_status,
            "valueFormatter": STATUS_FORMAT if is_status else NUMERIC_FORMAT
        }
        
        # Apply Status Colors if it's a status grid
        if is_status:
            col["cellStyle"] = {
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "flex-start", # Aligns text to the left
                "styleConditions": [
                    {"condition": "params.value == 0", "style": {"color": "#2b8a3e"}},
                    {"condition": "params.value < 0", "style": {"color": "#c92a2a"}}
                ]
            }
        cols.append(col)
        
    # Total Column (Pinned Right)
    total_col = {
        "headerName": "Total",
        "field": "row_total",
        "pinned": "right",
        "width": 90,
        "type": "numericColumn",
        "editable": False,
        "valueFormatter": STATUS_FORMAT if is_status else NUMERIC_FORMAT
    }
    
    if is_status:
        total_col["cellStyle"] = {
            "display": "flex", 
            "alignItems": "center", 
            "justifyContent": "flex-start",
            "styleConditions": [
                {"condition": "params.value == 0", "style": {"color": "#2b8a3e", "fontWeight": "bold"}},
                {"condition": "params.value < 0", "style": {"color": "#c92a2a", "fontWeight": "bold"}}
            ]
        }
    else:
        sum_logic = "params.data ? " + " + ".join([f"(Number(params.data.{m}) || 0)" for m in MONTHS]) + " : 0"
        total_col["valueGetter"] = {"function": sum_logic}
        total_col["cellStyle"] = {
            "fontWeight": "bold",
            "backgroundColor": f"{accent_color}15",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "flex-end"
        }
        
    cols.append(total_col)
    return cols

def create_grid(grid_id, header_name, is_status=False, accent_color="#228be6"):
    
    return dag.AgGrid(
        id=grid_id,
        columnDefs=_get_base_columns(header_name, is_status, accent_color),
        rowData=[{"Category": "Att allokera"}] if is_status else [],
        columnSize="responsiveSizeToFit", 
        defaultColDef={
            "resizable": False,
            "sortable": False,
            "suppressMovable": True,
            "cellStyle": {"display": "flex", "alignItems": "center"}
        },
        dashGridOptions={
            "headerHeight": 24,
            "rowHeight": 24,
            "domLayout": "autoHeight",
            "stopEditingWhenCellsLoseFocus": True,
            "pinnedBottomRowData": [{"Category": "Total"}] if not is_status else None,
        },
        style={
            "--ag-active-color": accent_color,
            "--ag-header-background-color": f"{accent_color}90" if not is_status else "#f8f9fa",
            "--ag-background-color": f"{accent_color}10" if not is_status else "#ffffff",
            "fontFamily": "'Inter', sans-serif", 
            "--ag-font-family": "'Inter', sans-serif",
        },
        className="ag-theme-balham",
        # Only apply custom row pinning styles to budget grids
        getRowStyle={
            "styleConditions": [
                {
                    "condition": "params.node.rowPinned === 'bottom'",
                    "style": {"fontWeight": "bold", "borderTop": f"2px solid {accent_color}"}
                }
            ]
        } if not is_status else None
    )
import dash
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, clientside_callback, ClientsideFunction, no_update
from database.db_manager import save_budget_to_db, load_budget_from_db
from components.budget_grids import MONTHS # is this best practice?


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
        new_row = {"Category": category_name, **{m: 0 for m in MONTHS}}
        
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
    Output("grid-status", "rowData"),
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
    prevent_initial_call='initial_duplicate' 
)
def populate_grids_on_load(selected_year):
    if not selected_year:
        return [], [], []
        
    inc_data, exp_data, sav_data = load_budget_from_db(int(selected_year))
    
    return inc_data, exp_data, sav_data
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    budget: {
        calculateAll: function(inc_data, exp_data, sav_data, c1, c2, c3, inc_opts, exp_opts, sav_opts) {
            if (!inc_opts || !exp_opts || !sav_opts) return window.dash_clientside.no_update;

            const months = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"];
            let inc_totals = {"Category": "Total"}, exp_totals = {"Category": "Total"}, sav_totals = {"Category": "Total"};
            
            // This will hold the data for our "Status Grid"
            let statusRow = {"Category": "Ofördelat"};
            let grand_diff = 0;

            months.forEach(m => {
                let inc = (inc_data || []).reduce((s, r) => s + (parseFloat(r[m]) || 0), 0);
                let exp = (exp_data || []).reduce((s, r) => s + (parseFloat(r[m]) || 0), 0);
                let sav = (sav_data || []).reduce((s, r) => s + (parseFloat(r[m]) || 0), 0);
                
                inc_totals[m] = inc; 
                exp_totals[m] = exp; 
                sav_totals[m] = sav;

                let diff = inc - exp - sav;
                statusRow[m] = diff; // Store the raw difference
                grand_diff += diff;
            });

            statusRow["row_total"] = grand_diff;

            return [
                [statusRow], // Return as an array for rowData
                {...inc_opts, "pinnedBottomRowData": [inc_totals]}, 
                {...exp_opts, "pinnedBottomRowData": [exp_totals]}, 
                {...sav_opts, "pinnedBottomRowData": [sav_totals]}
            ];
        }
    }
});
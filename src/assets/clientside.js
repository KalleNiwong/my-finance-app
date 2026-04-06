window.dash_clientside = Object.assign({}, window.dash_clientside, {
    budget: {
        // Added the three grid options as parameters at the end
        calculateAll: function(inc_data, exp_data, sav_data, c1, c2, c3, inc_opts, exp_opts, sav_opts) {
            
            // Safeguard against initial load where options might not be fully passed yet
            if (!inc_opts || !exp_opts || !sav_opts) return window.dash_clientside.no_update;

            const months = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"];
            
            let inc_totals = {"Category": "Total"};
            let exp_totals = {"Category": "Total"};
            let sav_totals = {"Category": "Total"};
            
            let statusElements = months.map(m => {
                let inc = (inc_data || []).reduce((s, r) => s + (parseFloat(r[m]) || 0), 0);
                let exp = (exp_data || []).reduce((s, r) => s + (parseFloat(r[m]) || 0), 0);
                let sav = (sav_data || []).reduce((s, r) => s + (parseFloat(r[m]) || 0), 0);
                
                inc_totals[m] = inc;
                exp_totals[m] = exp;
                sav_totals[m] = sav;

                let diff = inc - exp - sav;
                let color = diff === 0 ? "green" : "#c92a2a"; 
                let bg = diff === 0 ? '#ebfbee' : '#fff5f5';
                let icon = diff === 0 ? "✓" : "!";

                return `
                    <div style="border: 1px solid #dee2e6; padding: 2px 8px; border-radius: 4px; text-align: center; background: ${bg}; min-width: 60px;">
                        <div style="font-size: 10px; color: #868e96; text-transform: uppercase">${m}</div>
                        <div style="font-weight: bold; font-size: 12px; color: ${color}">${icon} ${diff.toLocaleString('sv-SE')}</div>
                    </div>
                `;
            }).join("");

            // Return the summary HTML, and the modified grid options
            return [
                // statusElements, 
                {...inc_opts, "pinnedBottomRowData": [inc_totals]}, 
                {...exp_opts, "pinnedBottomRowData": [exp_totals]}, 
                {...sav_opts, "pinnedBottomRowData": [sav_totals]}
            ];
        }
    }
});
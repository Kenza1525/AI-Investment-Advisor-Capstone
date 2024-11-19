// Mount Chainlit widget
window.mountChainlitWidget({
    chainlitServer: "http://localhost:8000"
});

// Handle Chainlit function calls
window.addEventListener("chainlit-call-fn", (e) => {
    const { name, args, callback } = e.detail;
    
    switch(name) {
        case "update_personal_info":
            updatePersonalInfo(args);
            callback("Personal information updated");
            break;
        
        case "update_allocation_chart":
            updateAllocationChart(args);
            callback("Allocation chart updated");
            break;
            
        case "update_forecast_charts":
            updateForecastCharts(args);
            callback("Forecast charts updated");
            break;
    }
});

// Function to update personal information fields
function updatePersonalInfo(data) {
    try {
        // Map data fields to form inputs
        const fieldMapping = {
            fullName: 'personal-name',
            job: 'personal-job',
            age: 'personal-age',
            phoneNumber: 'personal-phone',
            email: 'personal-email',
            investment_amount: 'investment-amount',
            time_horizon: 'investment-horizon'
        };

        // Update each field
        Object.entries(fieldMapping).forEach(([dataKey, elementId]) => {
            if (data[dataKey] !== undefined) {
                dash_clientside.set_props(elementId, {value: data[dataKey]});
            }
        });
    } catch (error) {
        console.error("Error updating personal information:", error);
    }
}

// Function to update the allocation pie chart
function updateAllocationChart(data) {
    try {
        const { allocation } = data;
        
        if (!allocation) {
            throw new Error("Missing allocation data");
        }

        const pieData = [{
            values: Object.values(allocation),
            labels: Object.keys(allocation),
            type: 'pie',
            hole: 0.4,
            marker: {
                colors: [
                    '#FF6B6B',  // Local equity
                    '#4ECDC4',  // Local bonds
                    '#45B7D1',  // Local cash
                    '#96CEB4'   // Global assets
                ]
            },
            textinfo: 'label+percent',
            hoverinfo: 'label+value+percent'
        }];

        const layout = {
            title: 'Portfolio Allocation',
            height: 400,
            width: 600,
            showlegend: false,
            margin: { t: 50, b: 0, l: 0, r: 0 }
        };

        Plotly.newPlot('allocation-chart', pieData, layout);

    } catch (error) {
        console.error("Error updating allocation chart:", error);
    }
}

// Function to update forecast charts
function updateForecastCharts(data) {
    try {
        const { lineChart, finalPieChart } = data;
        
        // Create line chart for growth projection
        const lineData = [];
        Object.entries(lineChart.asset_values).forEach(([assetClass, values], index) => {
            lineData.push({
                x: lineChart.years,
                y: values,
                name: assetClass,
                type: 'scatter',
                mode: 'lines+markers',
                marker: {
                    size: 8
                }
            });
        });

        const lineLayout = {
            title: 'Portfolio Growth Projection',
            xaxis: {
                title: 'Years',
                showgrid: true
            },
            yaxis: {
                title: 'Value',
                showgrid: true
            },
            height: 400,
            width: 800,
            showlegend: true,
            legend: {
                x: 1,
                xanchor: 'right',
                y: 1
            }
        };

        // Create pie chart for final allocation
        const pieData = [{
            values: Object.values(finalPieChart),
            labels: Object.keys(finalPieChart),
            type: 'pie',
            hole: 0.4,
            marker: {
                colors: [
                    '#FF6B6B',  // Local equity
                    '#4ECDC4',  // Local bonds
                    '#45B7D1',  // Local cash
                    '#96CEB4'   // Global assets
                ]
            },
            textinfo: 'label+percent',
            hoverinfo: 'label+value+percent'
        }];

        const pieLayout = {
            title: 'Final Portfolio Distribution',
            height: 400,
            width: 600,
            showlegend: false,
            margin: { t: 50, b: 0, l: 0, r: 0 }
        };

        // Plot both charts
        Plotly.newPlot('forecast-line-chart', lineData, lineLayout);
        Plotly.newPlot('forecast-pie-chart', pieData, pieLayout);

        // Store forecast data for reference
        const storageDiv = document.getElementById('forecast-data-storage');
        if (storageDiv) {
            storageDiv.textContent = JSON.stringify(data);
        }

    } catch (error) {
        console.error("Error updating forecast charts:", error);
    }
}

// Function to format currency values
function formatCurrency(value) {
    return new Intl.NumberFormat('en-ZA', {
        style: 'currency',
        currency: 'ZAR'
    }).format(value);
}

// Function to handle number formatting
function formatNumber(value, decimals = 2) {
    return new Intl.NumberFormat('en-ZA', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(value);
}

// Function to create custom legends
function createCustomLegend(elementId, data) {
    const legendContainer = document.getElementById(elementId);
    if (!legendContainer) return;

    legendContainer.innerHTML = Object.entries(data)
        .map(([label, value]) => `
            <div class="legend-item">
                <span class="legend-color" style="background-color: ${getColorForAsset(label)}"></span>
                <span class="legend-label">${label}</span>
                <span class="legend-value">${formatNumber(value)}%</span>
            </div>
        `)
        .join('');
}

// Helper function to get consistent colors for assets
function getColorForAsset(assetName) {
    const colorMap = {
        'Local equity': '#FF6B6B',
        'Local bonds': '#4ECDC4',
        'Local cash': '#45B7D1',
        'Global assets': '#96CEB4'
    };
    return colorMap[assetName] || '#CCCCCC';
}
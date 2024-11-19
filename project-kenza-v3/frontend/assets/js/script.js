// Constants
const COLORS = {
    'Local equity': '#FF6B6B',    // Red
    'Local bonds': '#FFD700',     // Yellow
    'Local cash': '#8A2BE2',      // Purple
    'Global assets': '#96CEB4'    // Green
};

const CHART_CONFIG = {
    allocation: {
        height: 450,
        width: 600,
        title: 'Portfolio Allocation'
    },
    forecast: {
        line: {
            height: 400,
            width: 700,
            title: 'Portfolio Growth Projection'
        },
        pie: {
            height: 400,
            width: 700,
            title: 'Final Portfolio Distribution'
        }
    }
};

// Initialize Chainlit widget
window.mountChainlitWidget({
    chainlitServer: "http://localhost:8000"
});

// Event Listeners
window.addEventListener("chainlit-call-fn", (e) => {
    const { name, args, callback } = e.detail;
    
    const handlers = {
        'update_personal_info': () => {
            updatePersonalInfo(args);
            callback("Personal information updated");
        },
        'update_allocation_chart': () => {
            updateAllocationChart(args);
            callback("Allocation chart updated");
        },
        'update_forecast_charts': () => {
            updateForecastCharts(args);
            callback("Forecast charts updated");
        }
    };

    handlers[name]?.();
});

// Utility Functions
function getColorForAsset(assetName) {
    return COLORS[assetName] || '#CCCCCC';
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-ZA', {
        style: 'currency',
        currency: 'ZAR'
    }).format(value);
}

function formatNumber(value, decimals = 2) {
    return new Intl.NumberFormat('en-ZA', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(value);
}

// Chart Creation Functions
function createPieChart(data, elementId, config) {
    const chartData = [{
        values: Object.values(data),
        labels: Object.keys(data),
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: Object.keys(data).map(asset => getColorForAsset(asset))
        },
        textinfo: 'label+percent',
        hoverinfo: 'label+value+percent'
    }];

    const layout = {
        title: config.title,
        height: config.height,
        width: config.width,
        showlegend: true,
        legend: {
            x: 1.1,
            y: 0.5
        },
        margin: { t: 50, b: 50, l: 20, r: 20 }
    };

    Plotly.newPlot(elementId, chartData, layout);
}

function createLineChart(data, years, elementId, config) {
    const lineData = Object.entries(data).map(([assetClass, values]) => ({
        x: years,
        y: values,
        name: assetClass,
        type: 'scatter',
        mode: 'lines+markers',
        marker: { size: 8 },
        line: { color: getColorForAsset(assetClass) }
    }));

    const layout = {
        title: config.title,
        height: config.height,
        width: config.width,
        xaxis: {
            title: 'Years',
            showgrid: true
        },
        yaxis: {
            title: 'Value',
            showgrid: true
        },
        showlegend: true,
        legend: {
            x: 1,
            xanchor: 'right',
            y: 1
        }
    };

    Plotly.newPlot(elementId, lineData, layout);
}

// Main Update Functions
function updatePersonalInfo(data) {
    try {
        const fieldMapping = {
            fullName: 'personal-name',
            job: 'personal-job',
            age: 'personal-age',
            phoneNumber: 'personal-phone',
            email: 'personal-email',
            investment_amount: 'investment-amount',
            time_horizon: 'investment-horizon'
        };

        Object.entries(fieldMapping).forEach(([dataKey, elementId]) => {
            if (data[dataKey] !== undefined) {
                dash_clientside.set_props(elementId, {value: data[dataKey]});
            }
        });
    } catch (error) {
        console.error("Error updating personal information:", error);
    }
}

function updateAllocationChart(data) {
    try {
        const { allocation } = data;
        if (!allocation) throw new Error("Missing allocation data");
        
        createPieChart(allocation, 'allocation-chart', CHART_CONFIG.allocation);
    } catch (error) {
        console.error("Error updating allocation chart:", error);
    }
}

function updateForecastCharts(data) {
    try {
        const { lineChart, finalPieChart } = data;
        
        // Create line chart
        createLineChart(
            lineChart.asset_values,
            lineChart.years,
            'forecast-line-chart',
            CHART_CONFIG.forecast.line
        );

        // Create pie chart
        createPieChart(
            finalPieChart,
            'forecast-pie-chart',
            CHART_CONFIG.forecast.pie
        );

        // Store forecast data
        const storageDiv = document.getElementById('forecast-data-storage');
        if (storageDiv) {
            storageDiv.textContent = JSON.stringify(data);
        }
    } catch (error) {
        console.error("Error updating forecast charts:", error);
    }
}

// Legend Creation
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
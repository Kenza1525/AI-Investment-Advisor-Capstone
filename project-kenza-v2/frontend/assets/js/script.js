// Mount Chainlit widget
window.mountChainlitWidget({
    chainlitServer: "http://localhost:8000"
});

// Handle Chainlit function calls
window.addEventListener("chainlit-call-fn", (e) => {
    const { name, args } = e.detail;

    // Only handle chart updates
    if (name === "update_chart") {
        updatePortfolioChart(args);
    }
});

// Function to update the portfolio chart
function updatePortfolioChart(chartData) {
    try {
        // Parse string data if needed
        const data = typeof chartData === 'string' ? JSON.parse(chartData) : chartData;
        
        if (!data?.allocation) {
            throw new Error("Missing allocation data");
        }

        // Create pie chart data
        const pieData = [{
            values: [
                data.allocation["Local equity"],
                data.allocation["Local bonds"],
                data.allocation["Local cash"],
                data.allocation["Global assets"]
            ],
            labels: [
                'Local equity',
                'Local bonds',
                'Local cash',
                'Global assets'
            ],
            type: 'pie',
            automargin: true
        }];

        // Chart layout configuration
        const layout = {
            height: 300,
            width: 450,
            margin: { "t": 0, "b": 0, "l": 0, "r": 0 }
        };

        // Create the plot
        Plotly.newPlot('portfolio-chart', pieData, layout);

        // Update storage for risk profile data
        const storageDiv = document.getElementById('risk-profile-data-storage');
        storageDiv.textContent = JSON.stringify(data.allocation);
    } catch (error) {
        console.error("Error updating portfolio chart:", error);
    }
}
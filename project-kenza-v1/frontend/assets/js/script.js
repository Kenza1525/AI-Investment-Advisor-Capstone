window.mountChainlitWidget({
    chainlitServer: "http://localhost:8000"
});

window.addEventListener("chainlit-call-fn", (e) => {
    const { name, args, callback } = e.detail;
    console.log("Chainlit call function triggered:", e.detail);  // Debugging line

    if (name === "update_chart") {
        console.log("Updating chart with data:", args);  // Debugging line
        try {
            if (typeof args === 'string') {
                args = JSON.parse(args);
            }
            if (args && args.allocation) {
                console.log("Parsed chart data:", args);  // Debugging line

                var data = [{
                    values: [
                        args.allocation["Local equity"], 
                        args.allocation["Local bonds"], 
                        args.allocation["Local cash"], 
                        args.allocation["Global assets"]],
                    labels: [
                        'Local equity', 
                        'Local bonds', 
                        'Local cash',
                        'Global assets'],
                    type: 'pie',
                    automargin: true,
                  }];
                  
                  var layout = {
                    height: 300,
                    width: 450,
                    margin: {"t": 0, "b": 0, "l": 0, "r": 0},
                    // showlegend: false
                  };
                  
                Plotly.newPlot('portfolio-chart', data, layout);

                const storageDiv = document.getElementById('risk-profile-data-storage');
                storageDiv.textContent = JSON.stringify(args.allocation);
                document.body.appendChild(storageDiv);

                // window.chartUpdater.updateChart(args);
                // callback("Chart updated successfully.");
            } else {
                console.error("Invalid chart data format:", args);  // Error log for invalid data
                // callback("Error: Invalid chart data format.");
            }
        } catch (error) {
            console.error("Error updating chart:", error);  // Error handling
            // callback(`Error: ${error.message}`);
        }
    }
});

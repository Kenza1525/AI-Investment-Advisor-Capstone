class ChartUpdater {
    constructor() {
        this.chartColors = {
            'Local equity': '#FF6B6B',
            'Local bonds': '#4ECDC4',
            'Local cash': '#45B7D1',
            'Global assets': '#96CEB4'
        };
    }

    updateChart(data) {
        if (!data || !data.allocation) return;
        const chartData = {
            data: [{
                type: 'pie',
                values: Object.values(data.allocation),
                labels: Object.keys(data.allocation),
                hole: 0.3,
                marker: {
                    colors: Object.keys(data.allocation).map(key => this.chartColors[key] || '#CCCCCC')
                },
                textinfo: 'label+percent',
                textposition: 'outside'
            }],
            layout: {
                title: {
                    text: `Asset Allocation for ${data.profile} Risk Profile`,
                    y: 0.95,
                    x: 0.5,
                    xanchor: 'center',
                    yanchor: 'top',
                    font: { size: 20, color: '#ffffff' }
                },
                showlegend: true,
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#ffffff' }
            }
        };

        if (window.dash_clientside) {
            console.log("Iyi dash client side", window.dash_clientside); // Debugging line
            window.dash_clientside.set_props("portfolio-chart", {figure: chartData});
        }
    }
}

window.chartUpdater = new ChartUpdater();
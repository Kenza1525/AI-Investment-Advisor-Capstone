import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import json

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ]
)

# Path to the feedback file
feedback_file = "feedback.jsonl"

def load_feedback():
    try:
        with open(feedback_file, "r") as file:
            return [json.loads(line) for line in file]
    except FileNotFoundError:
        return []

# Custom CSS
# Custom CSS update
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NexusWealth AI Feedback Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Righteous&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700&display=swap');
            
            body {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                margin: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                min-height: 100vh;
            }
            
            .custom-card {
                background: rgba(25, 25, 25, 0.9);
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td,
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            }
        </style>
        {%scripts%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout update
app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "color": "#ffffff",
        "padding": "2rem",
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    },
    children=[
        # Header Section
        html.Div(
            className="custom-card",
            style={
                "padding": "2rem",
                "marginBottom": "2rem",
                "textAlign": "center",
            },
            children=[
                html.H1(
                    "NexusWealth AI Feedback Dashboard",
                    style={
                        "fontFamily": '"Righteous", cursive',
                        "fontSize": "2.5rem",
                        "fontWeight": "700",
                        "marginBottom": "1rem",
                        "background": "linear-gradient(90deg, #00ff88 0%, #00d4ff 100%)",
                        "WebkitBackgroundClip": "text",
                        "WebkitTextFillColor": "transparent",
                    }
                ),
                html.P(
                    "Real-time feedback analysis and insights",
                    style={
                        "fontSize": "1.1rem",
                        "color": "#888888",
                        "margin": "0",
                    }
                )
            ]
        ),

        # Main Content
        html.Div(
            className="custom-card",
            style={"padding": "2rem"},
            children=[
                # Table Container
                html.Div(
                    style={"marginBottom": "2rem"},
                    children=[
                        dash_table.DataTable(
                            id="feedback-table",
                            style_table={
                                "borderRadius": "10px",
                                "overflow": "hidden",
                            },
                            style_data={
                                "backgroundColor": "rgba(25, 25, 25, 0.9)",
                                "color": "#ffffff",
                                "border": "none",
                                "fontSize": "0.9rem",
                                "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                            },
                            style_header={
                                "backgroundColor": "rgba(25, 25, 25, 0.9)",
                                "color": "#00ff88",
                                "fontWeight": "600",
                                "border": "none",
                                "fontSize": "1rem",
                                "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                            },
                            style_cell={
                                "textAlign": "left",
                                "padding": "1rem",
                                "borderBottom": "1px solid rgba(255, 255, 255, 0.1)",
                                "backgroundColor": "rgba(25, 25, 25, 0.9)",
                                "color": "#ffffff",
                            },
                            style_data_conditional=[
                                {
                                    "if": {"state": "selected"},
                                    "backgroundColor": "rgba(0, 255, 136, 0.2)",
                                    "border": "1px solid #00ff88",
                                }
                            ],
                            columns=[
                                {"name": "ID", "id": "id"},
                                {"name": "User Prompt", "id": "user_prompt"},
                                {"name": "Feedback", "id": "feedback"},
                                {
                                    "name": "Sentiment",
                                    "id": "value",
                                    "presentation": "markdown",
                                },
                            ],
                            markdown_options={"link_target": "_blank"},
                            page_size=10,
                        ),
                    ],
                ),

                # Download Button
                html.Button(
                    children=[
                        html.I(className="fas fa-download", style={"marginRight": "8px"}),
                        "Export Data"
                    ],
                    id="download-button",
                    style={
                        "background": "linear-gradient(90deg, #00ff88 0%, #00d4ff 100%)",
                        "color": "#1a1a1a",
                        "padding": "12px 24px",
                        "border": "none",
                        "borderRadius": "8px",
                        "cursor": "pointer",
                        "fontSize": "1rem",
                        "fontWeight": "600",
                        "display": "flex",
                        "alignItems": "center",
                        "margin": "0 auto",
                        "transition": "all 0.3s ease",
                        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                    },
                ),
                dcc.Download(id="download-dataframe-json"),
            ]
        ),
    ]
)

# Callback to load data into the table
@app.callback(
    Output("feedback-table", "data"),
    Input("feedback-table", "id"),
)
def update_table(_):
    feedback = load_feedback()
    for entry in feedback:
        entry["value"] = (
            "✅" if entry["value"] == 1 else "❌"
        )
    return feedback

# Callback for the download button
@app.callback(
    Output("download-dataframe-json", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_feedback(n_clicks):
    with open(feedback_file, "r") as file:
        data = file.read()
    return dict(content=data, filename="feedback.jsonl")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8080)


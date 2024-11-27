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
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Mandela Investments Feedback Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            body {
                background-color: #0a0a0f;
                margin: 0;
                font-family: 'Inter', sans-serif;
            }
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td {
                font-family: 'Inter', sans-serif !important;
            }
            .custom-card {
                background: linear-gradient(145deg, #131320, #1a1a2e);
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.05);
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

# App layout
app.layout = html.Div(
    style={
        "min-height": "100vh",
        "color": "#e0e0e0",
        "padding": "2rem",
    },
    children=[
        # Header Section
        html.Div(
            className="custom-card",
            style={
                "padding": "2rem",
                "margin-bottom": "2rem",
                "text-align": "center",
            },
            children=[
                html.H1(
                    "Mandela Investments Feedback Dashboard",
                    style={
                        "font-size": "2.5rem",
                        "font-weight": "700",
                        "margin-bottom": "1rem",
                        "background": "linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%)",
                        "-webkit-background-clip": "text",
                        "-webkit-text-fill-color": "transparent",
                    }
                ),
                html.P(
                    "Real-time feedback analysis and insights",
                    style={
                        "font-size": "1.1rem",
                        "color": "#8890b5",
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
                    style={"margin-bottom": "2rem"},
                    children=[
                        dash_table.DataTable(
                            id="feedback-table",
                            style_table={
                                "border-radius": "10px",
                                "overflow": "hidden",
                            },
                            style_data={
                                "backgroundColor": "#1a1a2e",
                                "color": "#e0e0e0",
                                "border": "none",
                                "font-size": "0.9rem",
                                "font-family": "'Inter', sans-serif",
                            },
                            style_header={
                                "backgroundColor": "#131320",
                                "color": "#00d2ff",
                                "fontWeight": "600",
                                "border": "none",
                                "font-size": "1rem",
                                "font-family": "'Inter', sans-serif",
                            },
                            style_cell={
                                "textAlign": "left",
                                "padding": "1rem",
                                "borderBottom": "1px solid #2a2a40",
                            },
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
                        html.I(className="fas fa-download", style={"margin-right": "8px"}),
                        "Export Data"
                    ],
                    id="download-button",
                    style={
                        "background": "linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%)",
                        "color": "white",
                        "padding": "12px 24px",
                        "border": "none",
                        "border-radius": "8px",
                        "cursor": "pointer",
                        "font-size": "1rem",
                        "font-weight": "500",
                        "display": "flex",
                        "align-items": "center",
                        "margin": "0 auto",
                        "transition": "transform 0.2s ease",
                        "hover": {
                            "transform": "translateY(-2px)"
                        }
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


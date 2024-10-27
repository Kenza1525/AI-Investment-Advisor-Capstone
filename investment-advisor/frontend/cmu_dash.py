# frontend/cmu_dash.py

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from frontend.components.login import login_layout
from frontend.components.signup import signup_layout

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Customizing the HTML structure for the app
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NexusWealth AI</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                min-height: 100vh;
                margin: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .login-container {
                background: rgba(25, 25, 25, 0.9);
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 2rem;
                width: 100%;
                max-width: 400px;
                margin: auto;
            }
            .title {
                color: #ffffff;
                font-size: 2.5rem;
                font-weight: 600;
                text-align: center;
                margin-bottom: 0.5rem;
                background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .subtitle {
                color: #888888;
                text-align: center;
                margin-bottom: 2rem;
            }
            .input-group {
                margin-bottom: 1.5rem;
            }
            .custom-input {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #ffffff;
                padding: 12px 15px;
                width: 100%;
                transition: all 0.3s ease;
            }
            .custom-input:focus {
                outline: none;
                border-color: #00ff88;
                box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
            }
            .button-container {
                display: flex;
                gap: 10px;
                justify-content: center;
            }
            .login-btn, .signup-btn {
                padding: 12px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 48%;
                border: none;
            }
            .login-btn {
                background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%);
                color: #1a1a1a;
            }
            .signup-btn {
                background: transparent;
                color: #00ff88;
                border: 2px solid #00ff88;
            }
            .login-btn:hover, .signup-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
            }
            .signup-btn:hover {
                background: rgba(0, 255, 136, 0.1);
            }
        </style>
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

# Define the app layout as a multi-page app
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),  # Track the current URL
        html.Div(id="page-content")             # Placeholder for page content
    ]
)

# Callback to update the page content based on the URL
@app.callback(
    dash.Output("page-content", "children"),
    [dash.Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/signup":
        return signup_layout
    elif pathname == "/login" or pathname == "/":
        return login_layout  # Default to login page
    else:
        return html.Div("404 - Page not found", style={'color': 'white', 'text-align': 'center', 'margin-top': '50px'})

# Running the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)

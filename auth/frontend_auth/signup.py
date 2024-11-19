from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from werkzeug.security import generate_password_hash, check_password_hash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dummy database
users = {}

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NexusWealth AI - Sign Up</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Righteous&display=swap');
            
            body {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                min-height: 100vh;
                margin: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .signup-container {
                background: rgba(25, 25, 25, 0.9);
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 2rem;
                width: 100%;
                max-width: 500px;
            }
            .title {
                font-family: 'Righteous', cursive;
                font-size: 2.5rem;
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
                font-size: 1.1rem;
            }
            .input-group {
                margin-bottom: 1.5rem;
            }
            .input-label {
                color: #ffffff;
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
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
            .custom-input::placeholder {
                color: rgba(255, 255, 255, 0.5);
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
                margin-top: 2rem;
            }
            .signup-btn, .back-btn {
                padding: 12px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
                border: none;
            }
            .signup-btn {
                background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%);
                color: #1a1a1a;
            }
            .back-btn {
                background: transparent;
                color: #00ff88;
                border: 2px solid #00ff88;
            }
            .signup-btn:hover, .back-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
            }
            .back-btn:hover {
                background: rgba(0, 255, 136, 0.1);
            }
            .error-message {
                color: #ff4444;
                font-size: 0.8rem;
                margin-top: 0.5rem;
                display: none;
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

app.layout = html.Div(
    className="d-flex justify-content-center align-items-center",
    style={"minHeight": "100vh"},
    children=[
        html.Div(
            className="signup-container",
            children=[
                html.H1("NexusWealth AI", className="title"),
                html.P("Create Your Account", className="subtitle"),
                
                # Username
                html.Div(
                    className="input-group",
                    children=[
                        html.Label("Username", className="input-label"),
                        dcc.Input(
                            type="text",
                            id="username",
                            className="custom-input",
                            placeholder="Choose a username"
                        ),
                        html.Div(id="username-error", className="error-message")
                    ]
                ),
                
                # Password
                html.Div(
                    className="input-group",
                    children=[
                        html.Label("Password", className="input-label"),
                        dcc.Input(
                            type="password",
                            id="password",
                            className="custom-input",
                            placeholder="Enter your password"
                        ),
                        html.Div(id="password-error", className="error-message")
                    ]
                ),
                
                # Repeat Password
                html.Div(
                    className="input-group",
                    children=[
                        html.Label("Confirm Password", className="input-label"),
                        dcc.Input(
                            type="password",
                            id="confirm-password",
                            className="custom-input",
                            placeholder="Repeat your password"
                        ),
                        html.Div(id="confirm-password-error", className="error-message")
                    ]
                ),
                
                # Buttons
                html.Div(
                    className="button-container",
                    children=[
                        html.Button(
                            "Create Account",
                            id="register-btn",
                            className="signup-btn"
                        ),
                        html.Button(
                            "Back to Login",
                            id="back-button",
                            className="back-btn"
                        )
                    ]
                ),
                dbc.Row(dbc.Col(html.Div(id="message"), className="subtitle text-center mt-4", style={"color": "green"})),
                dbc.Row(dbc.Col(html.Div(id="error"), className="subtitle text-center mt-4", style={"color": "red"})),
            ]
        )
    ]
)


@app.callback(
    Output("message", "children"),
    Output("error", "children"),
    Output("username", "value"),
    Output("password", "value"),
    Output("confirm-password", "value"),
    Input("register-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    State("confirm-password", "value")
)
def auth_process(register_clicks, username, password, confirm_password):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if not username or not password:
        return "", "", "", "", ""
    
    if triggered_id == "register-btn":
        if username in users:
            return "", "Username already exists. Please choose a different one.", "", "", ""
        elif password != confirm_password:
            return "", "Passwords do not match! try again", "", "", ""
        else:
            # Register user
            hashed_pw = generate_password_hash(password)
            users[username] = hashed_pw
            return "User registered successfully!", "", "", "", ""
    
    return "", "", "", "", ""

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)

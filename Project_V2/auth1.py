from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Simple Authentication"

# Simulated user storage (for testing purposes)
users = {}

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Login/Register Page"), className="text-center mb-4")),
    dcc.Location(id="url", refresh=False),
    
    # Login form
    dbc.Row(id="auth-page", children=[
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Label("Username")),
                dbc.Col(dbc.Input(id="username", placeholder="Enter your username", type="text"), width=12)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Password")),
                dbc.Col(dbc.Input(id="password", placeholder="Enter your password", type="password"), width=12)
            ], className="mb-3"),
            dbc.Button("Login", id="login-btn", color="primary", className="mr-2"),
            dbc.Button("Register", id="register-btn", color="secondary")
        ], width=4)
    ], justify="center"),

    # Message display
    dbc.Row(dbc.Col(html.Div(id="message"), className="text-center mt-4")),
])

# Callback for login/register
@app.callback(
    Output("message", "children"),
    Output("username", "value"),
    Output("password", "value"),
    Input("login-btn", "n_clicks"),
    Input("register-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value")
)
def auth_process(login_clicks, register_clicks, username, password):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if not username or not password:
        return "Please enter a username and password.", "", ""
    
    if triggered_id == "register-btn":
        if username in users:
            return "Username already exists. Please choose a different one.", "", ""
        else:
            # Register user
            hashed_pw = generate_password_hash(password)
            users[username] = hashed_pw
            return "User registered successfully!", "", ""
    
    elif triggered_id == "login-btn":
        # Authenticate user
        if username in users and check_password_hash(users[username], password):
            return "Logged in successfully!", "", ""
        else:
            return "Incorrect username or password.", "", ""
    return "", "", ""

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

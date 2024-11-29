import os
import json
from dash import Dash, html, dcc, Input, Output, State, callback_context, ClientsideFunction
import dash_bootstrap_components as dbc
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session
# from cmu_dash import layout
from cmu_dash_llm import layout_llm


external_stylesheets = [dbc.themes.BOOTSTRAP]
external_scripts = [
    'http://localhost:8000/copilot/index.js',
    'https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.27.1/plotly.min.js'
]

server = Flask(__name__)
server.secret_key = os.urandom(24)


app = Dash(__name__,
            server=server, 
          external_stylesheets=external_stylesheets,
          external_scripts=external_scripts,
          suppress_callback_exceptions=True)

app.title = "Simple Authentication"

# Dummy database
users = {'john': generate_password_hash('doe')}

# Custom HTML template
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NexusWealth AI</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="/assets/styles/custom.css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Righteous&display=swap');
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
            .custom-input::placeholder {
                color: rgba(255, 255, 255, 0.5);
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
                width: 100%;
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
        <div id="react-entry-point">
            {%app_entry%}
        </div>
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
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="userdata"),
        html.Div(
            className="login-container",
            children=[
                html.H1("NexusWealth AI", className="title"),
                html.P("Intelligent Investment Solutions", className="subtitle"),
                html.Div(
                    className="input-group",
                    children=[
                        dcc.Input(
                            id="username",
                            type="text",
                            placeholder="Username",
                            className="custom-input"
                        )
                    ]
                ),
                html.Div(
                    className="input-group",
                    children=[
                        dcc.Input(
                            id="password",
                            type="password",
                            placeholder="Password",
                            className="custom-input"
                        )
                    ]
                ),
                html.Div(
                    className="button-container",
                    children=[
                        html.Button(
                            "Login",
                            id="login-btn",
                            className="login-btn"
                        ),
                        html.Button(
                            "Sign Up",
                            id="register-btn",
                            className="signup-btn"
                        )
                    ]
                ),
                dbc.Row(dbc.Col(html.Div(id="message"), className="subtitle text-center mt-4")),
            ]
        ),
        html.Div(id="page-content-home"),
        html.Div(id='dummy-output', style={'display': 'none'})
    ]
)


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside', 
        function_name='redirect_to_home'
    ),
    Output('dummy-output', 'children'),
    Input('url', 'pathname')
)


# Callback for login/register
@app.callback(
    Output("url", "pathname"),
    Output("message", "children"),
    Output("username", "value"),
    Output("password", "value"),
    Output("userdata", "data"),
    Input("login-btn", "n_clicks"),
    Input("register-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value")
)
def auth_process(login_clicks, register_clicks, username, password):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == "register-btn":
        if not username or not password:
            return "", "Please enter a username and password!", "", "", ""
        if username in users:
            return "", "Username already exists! choose a different one", "", "", ""
        else:
            # Register user
            hashed_pw = generate_password_hash(password)
            users[username] = hashed_pw
            return "", "User registered successfully!", "", "", ""
    
    elif triggered_id == "login-btn":
        if not username or not password:
            return "", "Please enter a username and password!", "", "", ""
        # Authenticate user
        if username in users and check_password_hash(users[username], password):
            #session["username"] = username
            session["logged_in"] = True
            # Include JavaScript to force a page refresh
            # refresh_script = "window.location.reload();"
            return '/home', "", "", "", json.dumps({"username": username})
        else:
            return "", "Incorrect username or password!", "", "", ""
    return "", "", "", "", ""


# Callback for redirecting to the homepage app
@app.callback(
    Output("page-content-home", "children"),
    Input("url", "pathname"),
    Input("userdata", "data")
)
def redirect_to_home(pathname, userdata):
    if pathname == "" or pathname == "/":
        return ""
    elif pathname == "/home" and session.get("logged_in"):
        if userdata:
            data = json.loads(userdata)
            user = data.get("username", "")
            # layout(app, user)
            layout_llm(app, user)
    else:
        return html.Div("404 - Page not found")
    #return "Invalid URL"


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
import json
from dash import Dash, html, dcc, Input, Output, State, callback_context, ClientsideFunction
import dash_bootstrap_components as dbc
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session
# from cmu_dash import layout
from cmu_dash_llm import layout_llm
from users_db import register_user, verify_user


def login_layout():
    return html.Div(
        className="d-flex justify-content-center align-items-center",
        style={"minHeight": "100vh"},
        children=[
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="userdata"),
            html.Div(
                children=[
                    html.H1("NexusWealth AI", className="title"),
                    html.P("Intelligent Investment Solutions", className="subtitle"),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="username", type="text", placeholder="Username", className="custom-input")
                        ]
                    ),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="password", type="password", placeholder="Password", className="custom-input")
                        ]
                    ),
                    html.Div(
                        className="button-container",
                        children=[
                            html.Button("Login", id="login-btn", className="login-btn"),
                            html.Button("Sign Up", id="register-btn", className="signup-btn")
                        ]
                    ),
                    dbc.Row(dbc.Col(html.Div(id="message"), className="subtitle text-center mt-4")),
                ]
            ),
        ]
    )


def signup_layout():
    return html.Div(
        children=[
            dcc.Location(id="url-log", refresh=False),
            dcc.Store(id="signup-data"),
            html.Div(
                children=[
                    html.H1("NexusWealth AI", className="title"),
                    html.P("Create Your Account", className="subtitle"),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="fname", type="text", placeholder="First Name", className="custom-input")
                        ]
                    ),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="lname", type="text", placeholder="Last Name", className="custom-input")
                        ]
                    ),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="susername", type="text", placeholder="Select a username", className="custom-input")
                        ]
                    ),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="email", type="email", placeholder="Email address", className="custom-input")
                        ]
                    ),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="spassword", type="password", placeholder="Choose Password", className="custom-input")
                        ]
                    ),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="confirm_pass", type="password", placeholder="Confirm Password", autoComplete="off", className="custom-input")    
                        ]
                    ),
                    html.Div(
                        className="input-group",
                        children=[
                            dcc.Input(id="occupation", type="text", placeholder="Career Status e.g Recent Graduate, Retiree", className="custom-input")
                        ],
                    ),
                    html.Div(
                        className="custom-dropdown-input",
                        children=[
                            dcc.Dropdown(
                                id="occupation-d",
                                options=[
                                    {"label": "Recent Graduate", "value": "student"},
                                    {"label": "Working Professional", "value": "working"},
                                    {"label": "Retiree", "value": "retiree"},
                                    {"label": "Other", "value": "other"}
                                ],
                                placeholder="Career Status",
                                className="dropdown"
                            )
                        ]
                    ),
                    html.Div(
                        className="button-container",
                        children=[
                            html.Button(
                                "Register",
                                id="sregister-btn",
                                className="login-btn"
                            ),
                            html.Button(
                                "Back to Login",
                                id="back-login-btn",
                                className="signup-btn"
                            )
                        ]
                    ),
                    dbc.Row(dbc.Col(html.Div(id="message-signup"), className="subtitle text-center mt-4")),
                ]
            ),            
        ],
    )


def main_layout(app):

    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside', 
            function_name='redirect_to_home'
        ),
        Output('dummy-output', 'children'),
        Input('url', 'pathname')
    )

    # Custom HTML/CSS template
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
                .signup-container {
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
                .custom-dropdown { 
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    padding: 12px 15px;
                }
                .custom-dropdown-input {
                    margin-bottom: 1.5rem;
                }
                /* Dropdown container */
                .Select-control {
                    background-color: #fff;
                    border: 1px solid #ccc;
                    font-size: 14px;
                }
                /* Selected option text */
                .Select-value-label {
                    color: #007bff; /* Change this to your desired color */
                    font-weight: bold;
                }
                /* Placeholder text */
                .Select-placeholder {
                    color: #999;
                }
                /* Options dropdown menu */
                .Select-menu {
                    background-color: #f9f9f9;
                    color: #000;
                }
                .button-container {
                    display: flex;
                    gap: 10px;
                    justify-content: center;
                }
                .login-btn, .signup-btn, .back-login-btn, .sregister-btn {
                    padding: 12px;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    width: 100%;
                    border: none;
                }
                .login-btn, .sregister-btn {
                    background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%);
                    color: #1a1a1a;
                }
                .signup-btn, .back-login-btn {
                    background: transparent;
                    color: #00ff88;
                    border: 2px solid #00ff88;
                }
                .login-btn:hover, .signup-btn:hover, .back-login-btn:hover, .sregister-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
                }
                .signup-btn:hover, .back-login-btn:hover {
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

    # app.layout = html.Div([
    #     html.Div(id='login-container', children=login_layout(), style={"display": "block"}),
    #     html.Div(id='signup-container', children=signup_layout(), style={"display": "none"}),
    #     dcc.Location(id="url", refresh=False),
    #     html.Div(id='page-content-home'),
    #     html.Div(id='dummy-output', style={'display': 'none'})
    # ])

    app.layout = html.Div([
        html.Div([
            html.Div([], className="left-side", style={'width': '50%', 'background': 'url(./assets/img/investment.png) no-repeat center center', 'backgroundSize': 'cover'}),
            html.Div([
                html.Div(id='login-container', children=login_layout(), style={"display": "block"}),
                html.Div(id='signup-container', children=signup_layout(), style={"display": "none"}),
            ], className="right-side", style={'width': '50%'}),
        ], className="split-screen", style={'display': 'flex', 'height': '100vh'}),
        dcc.Location(id="url", refresh=False),
        html.Div(id='page-content-home'),
        html.Div(id='dummy-output', style={'display': 'none'})
    ])


    @app.callback(
        [Output('login-container', 'style'), Output('signup-container', 'style')],
        [Input('register-btn', 'n_clicks'), Input('back-login-btn', 'n_clicks')],
        prevent_initial_call=True
    )
    def toggle_form_visibility(register_clicks, back_login_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return {"display": "block"}, {"display": "none"} # Default: show login, hide signup
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'register-btn':
            return {"display": "none"}, {"display": "block"}  # Show signup, hide login
        elif button_id == 'back-login-btn':
            return {"display": "block"}, {"display": "none"}  # Show login, hide signup


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
        State("password", "value"),
    )
    def auth_process(login_clicks, register_clicks, username, password):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if triggered_id == "login-btn":
            if not username or not password:
                return "", "Please enter a username and password!", "", "", ""
            
            user_valid, user_id = verify_user(username, password)
            if user_valid:
                session["logged_in"] = True
                return '/home', "", "", "", json.dumps({"username": username})        
            else:
                return "", "Invalid username or password!", "", "", ""
        
        return "", "", "", "", ""


    @app.callback(
        [Output("url-log", "pathname"), Output("message-signup", "children"), Output("fname", "value"), Output("lname", "value"), Output("susername", "value"), Output("email", "value"), Output("spassword", "value"), Output("confirm_pass", "value")],
        [Input("sregister-btn", "n_clicks")],
        [State("fname", "value"), State("lname", "value"), State("susername", "value"), State("email", "value"), State("spassword", "value"), State("confirm_pass", "value"), State("occupation-d", "value")]
    )
    def signup_process(nclicks, fname, lname, susername, email, spassword, confirm_pass, occupation):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if not ctx.triggered:
            return "", "", "", "", "", "", "", ""
        
        elif triggered_id == "sregister-btn":
            if not fname or not lname or not susername or not email or not spassword or not confirm_pass or not occupation:
                return "", "Please fill in all fields!", fname, lname, susername, email, spassword, confirm_pass
            if spassword != confirm_pass:
                return "", "Passwords do not match! try again", fname, lname, susername, email, "", ""
            hashed_pw = generate_password_hash(spassword)
            success = register_user(susername, hashed_pw, fname, lname, email, occupation)
            if not success:
                return "/login", "Username already exists! choose a different one", fname, lname, "", email, "", ""
            return "/login", "Registered successfully! please go back and log in", "", "", "", "", "", ""
        
        return "", "", "", "", "", "", "", ""

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

    # @app.callback(
    #     [Output('login-container', 'style'), Output('signup-container', 'style'), Output('message', 'children')],
    #     [Input("url-log", "pathname"), Input("message-signup", "children")],
    # )
    # def redirect_to_login(pathname, message):
    #     if pathname == "/login":
    #         return {"display": "block"}, {"display": "none"}, message
    #     return {"display": "none"}, {"display": "block"}, ""


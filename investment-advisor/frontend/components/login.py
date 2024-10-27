# frontend/components/login.py

from dash import html, dcc
import dash_bootstrap_components as dbc

# Layout for login page
layout = html.Div(
    className="d-flex justify-content-center align-items-center",
    style={"minHeight": "100vh"},
    children=[
        html.Div(
            className="login-container",
            children=[
                html.H1("NexusWealth AI", className="title"),
                html.P("Intelligent Investment Solutions", className="subtitle"),
                html.Div(
                    className="input-group",
                    children=[
                        dcc.Input(
                            id="login-username",
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
                            id="login-password",
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
                            id="login-button",
                            className="login-btn"
                        ),
                        html.Button(
                            "Sign Up",
                            id="signup-button",
                            className="signup-btn"
                        )
                    ]
                )
            ]
        )
    ]
)

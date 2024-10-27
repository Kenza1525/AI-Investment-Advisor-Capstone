# frontend/components/signup.py

from dash import html, dcc
import dash_bootstrap_components as dbc

# Layout for signup page
layout = html.Div(
    className="d-flex justify-content-center align-items-center",
    style={"minHeight": "100vh"},
    children=[
        html.Div(
            className="login-container",
            children=[
                html.H1("NexusWealth AI", className="title"),
                html.P("Create Your Account", className="subtitle"),
                html.Div(
                    className="input-group",
                    children=[
                        dcc.Input(
                            id="signup-username",
                            type="text",
                            placeholder="Choose a username",
                            className="custom-input"
                        )
                    ]
                ),
                html.Div(
                    className="input-group",
                    children=[
                        dcc.Input(
                            id="signup-password",
                            type="password",
                            placeholder="Enter your password",
                            className="custom-input"
                        )
                    ]
                ),
                html.Div(
                    className="input-group",
                    children=[
                        dcc.Input(
                            id="signup-confirm-password",
                            type="password",
                            placeholder="Repeat your password",
                            className="custom-input"
                        )
                    ]
                ),
                html.Div(
                    className="button-container",
                    children=[
                        html.Button(
                            "Create Account",
                            id="signup-create-button",
                            className="login-btn"
                        ),
                        html.Button(
                            "Back to Login",
                            id="back-to-login-button",
                            className="signup-btn"
                        )
                    ]
                )
            ]
        )
    ]
)

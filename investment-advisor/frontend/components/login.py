# frontend/components/login.py
from dash import html, dcc

login_layout = html.Div(
    className="d-flex justify-content-center align-items-center",
    style={"minHeight": "100vh"},
    children=[
        html.Div(
            className="login-container",
            children=[
                html.H1(
                    "NexusWealth AI",
                    className="title",
                ),
                html.P(
                    "Intelligent Investment Solutions",
                    className="subtitle",
                ),
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
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "gap": "10px",
                        "width": "100%"
                    },
                    children=[
                        html.Button(
                            "Login",
                            id="login-button",
                            className="login-btn",
                            style={"flex": "1"}
                        ),
                        html.A(
                            html.Button(
                                "Sign Up",
                                id="signup-button",
                                className="signup-btn",
                                style={"flex": "1", "width": "100%"}
                            ),
                            href="/signup",
                            style={"flex": "1", "textDecoration": "none"}
                        )
                    ]
                ),
                html.Div(id="login-feedback", className="subtitle", style={"marginTop": "20px"})
            ]
        )
    ]
)

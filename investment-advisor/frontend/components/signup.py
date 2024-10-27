# frontend/components/signup.py
from dash import html, dcc

signup_layout = html.Div(
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
                    "Create Your Account",
                    className="subtitle",
                ),
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
                            id="signup-password-confirm",
                            type="password",
                            placeholder="Repeat your password",
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
                            "Create Account",
                            id="create-account-button",
                            className="login-btn",
                            style={"flex": "1"}
                        ),
                        html.A(
                            html.Button(
                                "Back to Login",
                                id="back-to-login-button",
                                className="signup-btn",
                                style={"flex": "1", "width": "100%"}
                            ),
                            href="/login",
                            style={"flex": "1", "textDecoration": "none"}
                        )
                    ]
                ),
                html.Div(id="signup-feedback", className="subtitle", style={"marginTop": "20px"})
            ]
        )
    ]
)
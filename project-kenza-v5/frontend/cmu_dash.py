from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json


def create_sidebar():
    return html.Div(
        className="sidebar",
        children=[
            html.Div([
                html.H1("NexusWealth", className="logo-text"),
                html.H2("AI", className="logo-subtext")
            ], className="logo-container"),
            html.Button("🏠 Home", id="btn-home", className="nav-button"),
            html.Button("📚 Education", id="btn-education", className="nav-button"),
            html.Button("📊 Asset Allocation", id="btn-allocation", className="nav-button"),
        ]
    )

def create_home_content(user="User"):
    username = user
    return html.Div([
        html.H1(f"Welcome to NexusWealth AI, {username}", className="section-title"),
        html.P(
            "Your intelligent financial companion for informed investment decisions "
            "and personalized portfolio management.",
            className="section-description"
        )
    ], className="home-container")

def create_education_content():
    return html.Div([
        html.H2("Investment Education", className="section-title"),
        html.P(
            "Explore investment topics and get personalized guidance from our AI assistant.",
            className="section-description"
        ),
        html.Div([
            html.Div([
                html.H3("Investment Basics", className="card-title"),
                html.P("Learn about stocks, bonds, mutual funds, and ETFs", className="card-text")
            ], className="feature-card"),
            html.Div([
                html.H3("Risk Management", className="card-title"),
                html.P("Understand portfolio diversification and risk assessment", className="card-text")
            ], className="feature-card"),
            html.Div([
                html.H3("Market Analysis", className="card-title"),
                html.P("Get insights on market trends and analysis techniques", className="card-text")
            ], className="feature-card")
        ], className="feature-grid")
    ], className="education-container")

def create_allocation_content():
    return html.Div(
        className="allocation-container",
        children=[
            # Left Column
            html.Div(className="left-panel", children=[
                # Personal Information Section
                html.Div(className="personal-info-section", children=[
                    html.H2("Personal Information", className="section-title"),
                    html.Div(className="form-container", children=[
                        html.Div(className="form-group", children=[
                            html.Label("Full Name", className="form-label"),
                            dcc.Input(id='personal-name', type="text", className="form-input",
                                    placeholder="Enter your full name")
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Job", className="form-label"),
                            dcc.Input(id='personal-job', type="text", className="form-input",
                                    placeholder="Enter your occupation")
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Age", className="form-label"),
                            dcc.Input(id='personal-age', type="number", className="form-input",
                                    placeholder="Enter your age")
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Phone Number", className="form-label"),
                            dcc.Input(id='personal-phone', type="tel", className="form-input",
                                    placeholder="Enter your phone number")
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Email", className="form-label"),
                            dcc.Input(id='personal-email', type="email", className="form-input",
                                    placeholder="Enter your email address")
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Investment Amount", className="form-label"),
                            dcc.Input(id='investment-amount', type="number", className="form-input",
                                    placeholder="Enter investment amount")
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Investment Horizon (Years)", className="form-label"),
                            dcc.Input(id='investment-horizon', type="number", className="form-input",
                                    placeholder="Enter number of years")
                        ])
                    ])
                ]),
                
                # Portfolio Distribution Section
                html.Div(className="portfolio-section", children=[
                    html.H2("Portfolio Distribution", className="section-title"),
                    html.Div(id="allocation-chart")
                ])
            ]),
            
            # Right Column - Forecasting
            html.Div(className="right-panel", children=[
                html.H2("Portfolio Forecasting", className="section-title"),
                # Growth Projection
                html.Div(className="forecast-section", children=[
                    html.H3("Growth Projection", className="section-subtitle"),
                    html.Div(id="forecast-line-chart", className="forecast-chart")
                ]),
                # Final Distribution
                html.Div(className="forecast-section", children=[
                    html.H3("Final Portfolio Distribution", className="section-subtitle"),
                    html.Div(id="forecast-pie-chart", className="forecast-chart")
                ]),
                # Summary
                #html.Div(id="forecast-summary", className="forecast-summary")
            ])
        ]
    )

def layout(app, username):
    # Main layout
    app.layout = html.Div(
        className="app-container",
        children=[
            create_sidebar(),
            html.Div(className="main-content", children=[
                html.Div(id="page-content", children=create_home_content(username))
            ]),
            # Storage components
            html.Div(id='risk-profile-data-storage', style={'display': 'none'}),
            html.Div(id='forecast-data-storage', style={'display': 'none'}),
            dcc.Store(id='personal-info-store'),
            dcc.Store(id='allocation-store'),
            dcc.Store(id='forecast-store')
        ]
    )

    @app.callback(
        Output("page-content", "children"),
        [Input("btn-home", "n_clicks"),
        Input("btn-education", "n_clicks"),
        Input("btn-allocation", "n_clicks")]
    )
    def update_page(home_clicks, edu_clicks, alloc_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return create_home_content(username)
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "btn-home":
            return create_home_content(username)
        elif button_id == "btn-education":
            return create_education_content()
        elif button_id == "btn-allocation":
            return create_allocation_content()
        return create_home_content(username)

    @app.callback(
        [Output('personal-name', 'value'),
        Output('personal-job', 'value'),
        Output('personal-age', 'value'),
        Output('personal-phone', 'value'),
        Output('personal-email', 'value'),
        Output('investment-amount', 'value'),
        Output('investment-horizon', 'value')],
        [Input('personal-info-store', 'data')]
    )
    def update_form_fields(stored_data):
        if stored_data:
            data = json.loads(stored_data)
            return [
                data.get('fullName', ''),
                data.get('job', ''),
                data.get('age', ''),
                data.get('phoneNumber', ''),
                data.get('email', ''),
                data.get('investment_amount', ''),
                data.get('time_horizon', '')
            ]
        return [''] * 7

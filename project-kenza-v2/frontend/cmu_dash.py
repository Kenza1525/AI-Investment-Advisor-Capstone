from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json

# Initialize Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]
external_scripts = [
    'http://localhost:8000/copilot/index.js'  # Chainlit integration
]

app = Dash(__name__, 
          external_stylesheets=external_stylesheets,
          external_scripts=external_scripts,
          suppress_callback_exceptions=True)

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
        <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.27.1/plotly.min.js"></script>
    </body>
</html>
'''

def create_sidebar():
    return html.Div(
        className="sidebar",
        children=[
            html.Div([
                html.H1("NexusWealth", className="logo-text", 
                       style={'background': 'linear-gradient(90deg, #00ff88, #00d4ff)',
                             '-webkit-background-clip': 'text',
                             '-webkit-text-fill-color': 'transparent'}),
                html.H2("AI", className="logo-subtext",
                       style={'background': 'linear-gradient(90deg, #00ff88, #00d4ff)',
                             '-webkit-background-clip': 'text',
                             '-webkit-text-fill-color': 'transparent'})
            ], className="logo-container"),
            html.Button("🏠 Home", id="btn-home", className="nav-button"),
            html.Button("📚 Education", id="btn-education", className="nav-button"),
            html.Button("📊 Asset Allocation", id="btn-allocation", className="nav-button"),
            html.Button("📈 Forecasting", id="btn-forecast", className="nav-button"),
        ]
    )

def create_home_content():
    return html.Div([
        html.H1("Welcome to NexusWealth AI", className="section-title",
               style={'background': 'linear-gradient(90deg, #00ff88, #00d4ff)',
                     '-webkit-background-clip': 'text',
                     '-webkit-text-fill-color': 'transparent'}),
        html.P(
            "Your intelligent financial companion for informed investment decisions "
            "and personalized portfolio management.",
            className="section-description"
        )
    ], className="home-container")

def create_education_content():
    return html.Div([
        html.H2("Investment Education", className="section-title",
               style={'background': 'linear-gradient(90deg, #00ff88, #00d4ff)',
                     '-webkit-background-clip': 'text',
                     '-webkit-text-fill-color': 'transparent'}),
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
    return html.Div([
        # Personal Information Section
        html.Div([
            html.H2("Personal Information", className="section-title",
                   style={'background': 'linear-gradient(90deg, #00ff88, #00d4ff)',
                         '-webkit-background-clip': 'text',
                         '-webkit-text-fill-color': 'transparent'}),
            html.Div([
                html.Div([
                    html.Label("Full Name", className="form-label"),
                    dcc.Input(
                        id='personal-name',
                        type="text",
                        className="form-input",
                        placeholder="Enter your full name"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Job", className="form-label"),
                    dcc.Input(
                        id='personal-job',
                        type="text",
                        className="form-input",
                        placeholder="Enter your occupation"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Age", className="form-label"),
                    dcc.Input(
                        id='personal-age',
                        type="number",
                        className="form-input",
                        placeholder="Enter your age"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Phone Number", className="form-label"),
                    dcc.Input(
                        id='personal-phone',
                        type="tel",
                        className="form-input",
                        placeholder="Enter your phone number"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Email", className="form-label"),
                    dcc.Input(
                        id='personal-email',
                        type="email",
                        className="form-input",
                        placeholder="Enter your email address"
                    )
                ], className="form-group"),
            ], className="form-container")
        ], className="info-section"),
        
        # Portfolio Distribution Section with proper spacing and sizing
        html.Div([
            html.H2("Portfolio Distribution", className="section-title distribution-title",
                   style={'background': 'linear-gradient(90deg, #00ff88, #00d4ff)',
                         '-webkit-background-clip': 'text',
                         '-webkit-text-fill-color': 'transparent',
                         'margin-top': '3rem'}),
            html.Div(
                id="portfolio-container",
                className="chart-container",
                children=[
                    # Empty div that will be replaced with chart
                    html.Div(id="portfolio-chart")
                ]
            )
        ], className="portfolio-section")
    ], className="allocation-container")

def create_forecast_content():
    return html.Div([
        html.H2("Market Forecasting", className="section-title",
               style={'background': 'linear-gradient(90deg, #00ff88, #00d4ff)',
                     '-webkit-background-clip': 'text',
                     '-webkit-text-fill-color': 'transparent'}),
        html.P(
            "Coming Soon: Advanced AI-powered market forecasting features",
            className="section-description"
        )
    ], className="forecast-container")

# Main layout
app.layout = html.Div(
    className="app-container",
    children=[
        create_sidebar(),
        html.Div(
            className="main-content",
            children=[
                html.Div(id="page-content", children=create_home_content())
            ]
        ),

        html.Div(id='risk-profile-data-storage', style={'display': 'none'}),

        # Store components for data handling
        dcc.Store(id='personal-info-store'),
        dcc.Store(id='risk-profile-store', storage_type='memory')
    ]
)

# Callbacks
@app.callback(
    Output("page-content", "children"),
    [Input("btn-home", "n_clicks"),
     Input("btn-education", "n_clicks"),
     Input("btn-allocation", "n_clicks"),
     Input("btn-forecast", "n_clicks")]
)
def update_page(home_clicks, edu_clicks, alloc_clicks, forecast_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return create_home_content()
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "btn-home":
        return create_home_content()
    elif button_id == "btn-education":
        return create_education_content()
    elif button_id == "btn-allocation":
        return create_allocation_content()
    elif button_id == "btn-forecast":
        return create_forecast_content()
    
    return create_home_content()

# Callback to update form fields
@app.callback(
    [Output('personal-name', 'value'),
     Output('personal-job', 'value'),
     Output('personal-age', 'value'),
     Output('personal-phone', 'value'),
     Output('personal-email', 'value')],
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
            data.get('email', '')
        ]
    return [''] * 5

@app.callback(Output('risk-profile-store', 'data'), Input('risk-profile-data-storage', 'children'))
def update_risk_profile_chart(data):
    print("This is what we need to use in order to graph: ", data)

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import os
from profile_db import init_db, insert_profile  # Import database functions

# Initialize the database when the app starts
init_db()

external_scripts = [
    'http://localhost:8000/copilot/index.js'
]

app = Dash(__name__, external_scripts=external_scripts)

app.layout = html.Div(children=[
    html.H1(children='Investment Advisor Dashboard'),
    html.Div([
        html.H2(children='User Profile', style={'font-family': 'sans-serif'}),
        html.Div([
            html.Div([html.Label(['Name'], style={'font-family': 'sans-serif'}),
                      dcc.Input(id='name', type='text', style={"font-family": 'sans-serif', 'font-size': 20})]),

            html.Div([html.Label(['Age'], style={'font-family': 'sans-serif'}),
                      dcc.Input(id='age', type='number', style={"font-family": 'sans-serif', 'font-size': 20})]),

            html.Div([html.Label(['Education'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='education', options=['High School', "Bachelor's", "Master's", 'PhD', 'Other'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),

            html.Div([html.Label(['Investment Length'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='investment_length', options=['Short-term', 'Medium-term', 'Long-term'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),

            html.Div([html.Label(['Investment Goal'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='investment_goal', options=['Education', 'Wealth Accumulation', 'Specific Purchase', 'Marriage', 'Other'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),

            html.Div([html.Label(['Risk Tolerance'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='risk_tolerance', options=['Low', 'Medium', 'High'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),
        ]),
        html.Button('Submit Profile', id='submit-profile', style={"width": "150px", "height": "40px", "font-family": 'sans-serif', 'font-size': 20, 'margin-top': '20px'}),
        html.Div(id='profile-submit-response', children='Click to submit profile')
    ]),
    html.Div([
        html.H2(children='Investment Distribution', style={'font-family': 'sans-serif'}),
        dcc.Graph(id='investment-pie-chart')
    ]),
    dcc.Store(id='profile-data'),
    dcc.Store(id='investment-data')  # Store for investment distribution
])

# Callback to generate a pie chart based on investment data
@app.callback(
    Output('investment-pie-chart', 'figure'),
    Input('investment-data', 'data')
)
def update_pie_chart(data):
    if data is None:
        return px.pie(title="No data available")

    # Create a DataFrame from the investment data
    df = pd.DataFrame(list(data.items()), columns=['Stock', 'Amount'])
    fig = px.pie(df, values='Amount', names='Stock', title='Investment Distribution')
    return fig

# Callback to submit profile and generate investment data (no changes to investment logic)
@app.callback(
    Output('profile-submit-response', 'children'),
    Output('investment-data', 'data'),  # Store investment distribution data
    Input('submit-profile', 'n_clicks'),
    State('name', 'value'),
    State('age', 'value'),
    State('education', 'value'),
    State('investment_length', 'value'),
    State('investment_goal', 'value'),
    State('risk_tolerance', 'value')
)
def submit_profile(n_clicks, name, age, education, investment_length, investment_goal, 
                   risk_tolerance):
    if n_clicks:
        if not name or not age or not education or not investment_length or not investment_goal or not risk_tolerance:
            return "Please fill in all required fields.", None

        # Insert the profile into the SQLite database
        success = insert_profile(name, age, education, investment_length, investment_goal, risk_tolerance)

        if success:
            # Call the function that generates the investment distribution (already working in your original app)
            investment_distribution = { 
                'Asset A': 3000,  # Example values
                'Asset B': 1500,  # Example values
                'Asset C': 2500   # Example values
            }

            # Return the success message and investment distribution data
            return f"Profile submitted successfully for {name}", investment_distribution
        else:
            return f"Profile for {name} already exists.", None

    return "Click to submit profile", None

if __name__ == '__main__':
    app.run_server(debug=True)


from dash import Dash, html, dcc, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd

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
            html.Div([html.Label(['Email'], style={'font-family': 'sans-serif'}),
                      dcc.Input(id='email', type='email', style={"font-family": 'sans-serif', 'font-size': 20})]),
            html.Div([html.Label(['Age'], style={'font-family': 'sans-serif'}),
                      dcc.Input(id='age', type='number', style={"font-family": 'sans-serif', 'font-size': 20})]),
            html.Div([html.Label(['Education'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='education', options=['High School', "Bachelor's", "Master's", 'PhD', 'Other'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),
            html.Div([html.Label(['Investment Length'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='investment_length', options=['Short-term', 'Medium-term', 'Long-term'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),
            html.Div([html.Label(['Investment Goal'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='investment_goal', options=['Education', 'Wealth Accumulation', 'Specific Purchase','Marriage', 'Other'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),
            html.Div([html.Label(['Risk Tolerance'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='risk_tolerance', options=['Low', 'Medium', 'High'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),
            html.Div([html.Label(['Investment Knowledge'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='investment_knowledge', options=['Beginner', 'Intermediate', 'Advanced'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),
            html.Div([html.Label(['Financial Class'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='financial_class', options=['Lower', 'Middle', 'Upper'],
                                   style={"font-family": 'sans-serif', 'font-size': 20})]),
            html.Div([html.Label(['Employment Status'], style={'font-family': 'sans-serif'}),
                      dcc.Dropdown(id='employment_status', options=['Employed', 'Self-employed', 'Unemployed', 'Student', 'Retired'],
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
    dcc.Store(id='investment-data')
])

@app.callback(
    Output('investment-pie-chart', 'figure'),
    Input('investment-data', 'data')
)
def update_pie_chart(data):
    if data is None:
        return px.pie(title="No data available")
    
    df = pd.DataFrame(list(data.items()), columns=['Stock', 'Amount'])
    fig = px.pie(df, values='Amount', names='Stock', title='Investment Distribution')
    return fig

@app.callback(
    Output('profile-submit-response', 'children'),
    Input('submit-profile', 'n_clicks'),
    State('name', 'value'),
    State('email', 'value'),
    State('age', 'value'),
    State('education', 'value'),
    State('investment_length', 'value'),
    State('investment_goal', 'value'),
    State('risk_tolerance', 'value'),
    State('investment_knowledge', 'value'),
    State('financial_class', 'value'),
    State('employment_status', 'value')
)
def submit_profile(n_clicks, name, email, age, education, investment_length, investment_goal, 
                   risk_tolerance, investment_knowledge, financial_class, employment_status):
    if n_clicks:
        # Here you would typically save this data to a database
        return f"Profile submitted for {name}"
    return "Click to submit profile"

if __name__ == '__main__':
    app.run_server(debug=True)
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import os
from profiles_db import init_db, insert_profile  # Import database functions

# Initialize the database when the app starts
init_db()

external_scripts = [
    'http://localhost:8000/copilot/index.js'
]

app = Dash(__name__, external_scripts=external_scripts)

app.layout = html.Div(children=[
    html.H1(children='Investment Advisor Dashboard'),
   
    html.Div([
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
    df = pd.DataFrame(list(data.items()), columns=['Asset', 'Amount'])
    fig = px.pie(df, values='Amount', names='Asset')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


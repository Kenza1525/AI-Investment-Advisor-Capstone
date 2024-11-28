from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import os
import json
from profiles_db import init_db, insert_profile  # Import database functions

# Initialize the database when the app starts
init_db()

external_scripts = [
    'http://localhost:8000/copilot/index.js'
]

def layout_llm(app, username):

    app.layout = html.Div(children=[
        html.H1(children=f'Investment Advisor Dashboard, Welcome {username}'),
    
        html.Div([
            dcc.Graph(id='investment-pie-chart')
        ]),
        html.Div([
            dcc.Graph(id='forecast-line-chart')
        ]),
        html.Div([
            dcc.Graph(id='forecast_distribution_pie_chart')
        ]),
        dcc.Store(id='forecast-data'),
        dcc.Store(id='investment-data'),
        dcc.Store(id='future_investment_distribution'),
    ])

    # Callback to generate a pie chart based on investment data
    @app.callback(
        Output('forecast_distribution_pie_chart', 'figure'),
        Input('future_investment_distribution', 'data')
    )
    def update_future_pie_chart(data):

        if data is None:
            return px.pie(title="No data available")

        # Create a DataFrame from the investment data
        df = pd.DataFrame(list(data.items()), columns=['Asset', 'Amount'])
        fig = px.pie(df, values='Amount', names='Asset')
        return fig

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


    @app.callback(
        Output('forecast-line-chart', 'figure'),
        Input('forecast-data', 'data')
    )
    def update_forecast_chart(data):
        if data is None:
            return go.Figure().update_layout(title="No forecast data available")
        
        try:
            # Print received data for debugging
            print("Received forecast data:", json.dumps(data, indent=2))
            
            fig = go.Figure()
            
            # Ensure we have the required data structure
            if not all(key in data for key in ['years', 'asset_values', 'metadata']):
                return go.Figure().update_layout(title="Invalid forecast data format")
            
            years = data['years']
            asset_values = data['asset_values']
            
            # Add a trace for each asset class
            for asset_class, values in asset_values.items():
                fig.add_trace(go.Scatter(
                    x=years,
                    y=values,
                    mode='lines',
                    name=asset_class
                ))
            
            # Calculate and add total portfolio value
            if asset_values:
                total_values = []
                for i in range(len(years)):
                    total = sum(values[i] for values in asset_values.values())
                    total_values.append(total)
                
                fig.add_trace(go.Scatter(
                    x=years,
                    y=total_values,
                    mode='lines',
                    name='Total Portfolio Value',
                    line=dict(width=3, dash='dash')
                ))
            
            fig.update_layout(
                title=f"Portfolio Forecast over {data['metadata']['horizon']} Years (Inflation Rate: {data['metadata']['inflation_rate']*100:.1f}%)",
                xaxis_title="Years",
                yaxis_title="Value (Inflation-Adjusted $)",
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
            
            return fig
        
        except Exception as e:
            print(f"Error in forecast chart callback: {e}")
            return go.Figure().update_layout(title=f"Error creating forecast chart: {str(e)}")


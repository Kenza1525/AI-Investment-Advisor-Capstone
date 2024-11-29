from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import os
import json
from profiles_db import init_db, insert_profile

# Initialize the database when the app starts
init_db()

external_scripts = [
    'http://localhost:8000/copilot/index.js'
]

def layout_llm(app, username):
    # Define the common chart theme to match the login page aesthetic

    asset_colors = ['#FF6B6B', '#FFD700', '#8A2BE2', '#96CEB4']

    # asset_colors = {
    # 'Local equity': '#FF6B6B',    # Red
    # 'Local bonds': '#FFD700',     # Yellow
    # 'Local cash': '#8A2BE2',      # Purple
    # 'Global assets': '#96CEB4'    # Green
    # }

    chart_theme = {
        'template': 'plotly_dark',
        'paper_bgcolor': 'rgba(25, 25, 25, 0.9)',
        'plot_bgcolor': 'rgba(25, 25, 25, 0.9)',
        'font': {
            'family': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
            'color': '#888888'
        }
    }

    app.layout = html.Div(
        style={
            'background': 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
            'minHeight': '100vh',
            'padding': '2rem',
            'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
            'color': '#ffffff'
        },
        children=[
            html.H1(
                f'Welcome, {username}',
                style={
                    'fontFamily': '"Righteous", cursive',
                    'fontSize': '2.5rem',
                    'textAlign': 'center',
                    'marginBottom': '0.5rem',
                    'background': 'linear-gradient(90deg, #00ff88 0%, #00d4ff 100%)',
                    'WebkitBackgroundClip': 'text',
                    'WebkitTextFillColor': 'transparent',
                    # 'textShadow': '0 0 10px rgba(0, 255, 136, 0.5), 0 0 20px rgba(0, 255, 136, 0.3), 0 0 30px rgba(0, 255, 136, 0.2)'
                    # 'animation': 'glow 1.5s ease-in-out infinite alternate'
                }
            ),
            html.H2(
                'Investment Dashboard',
                style={
                    'color': '#888888',
                    'textAlign': 'center',
                    'marginBottom': '2rem',
                    'fontSize': '1.1rem'
                }
            ),
            html.Div([
                html.Div(
                    className="chart-container",
                    style={
                        'background': 'rgba(25, 25, 25, 0.9)',
                        'borderRadius': '15px',
                        'boxShadow': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
                        'backdropFilter': 'blur(4px)',
                        'border': '1px solid rgba(255, 255, 255, 0.1)',
                        'padding': '1.5rem',
                        'marginBottom': '2rem'
                    },
                    children=[
                        dcc.Graph(
                            id='investment-pie-chart',
                            config={'displayModeBar': False}
                        )
                    ]
                ),
                html.Div(
                    className="chart-container",
                    style={
                        'background': 'rgba(25, 25, 25, 0.9)',
                        'borderRadius': '15px',
                        'boxShadow': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
                        'backdropFilter': 'blur(4px)',
                        'border': '1px solid rgba(255, 255, 255, 0.1)',
                        'padding': '1.5rem',
                        'marginBottom': '2rem'
                    },
                    children=[
                        dcc.Graph(
                            id='forecast-line-chart',
                            config={'displayModeBar': False}
                        )
                    ]
                ),
                html.Div(
                    className="chart-container",
                    style={
                        'background': 'rgba(25, 25, 25, 0.9)',
                        'borderRadius': '15px',
                        'boxShadow': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
                        'backdropFilter': 'blur(4px)',
                        'border': '1px solid rgba(255, 255, 255, 0.1)',
                        'padding': '1.5rem'
                    },
                    children=[
                        dcc.Graph(
                            id='forecast_distribution_pie_chart',
                            config={'displayModeBar': False}
                        )
                    ]
                )
            ]),
            dcc.Store(id='forecast-data'),
            dcc.Store(id='investment-data'),
            dcc.Store(id='future_investment_distribution'),
        ]
    )

    @app.callback(
        Output('forecast_distribution_pie_chart', 'figure'),
        Input('future_investment_distribution', 'data')
    )
    def update_future_pie_chart(data):
        if data is None:
            return px.pie(title="No data available").update_layout(**chart_theme)

        df = pd.DataFrame(list(data.items()), columns=['Asset', 'Amount'])
        fig = px.pie(
            df,
            values='Amount',
            names='Asset',
            color='Asset',
            color_discrete_sequence=asset_colors
        )
        
        fig.update_layout(
            **chart_theme,
            title={
                'text': "Future Investment Distribution",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        return fig

    @app.callback(
        Output('investment-pie-chart', 'figure'),
        Input('investment-data', 'data')
    )
    def update_pie_chart(data):
        if data is None:
            return px.pie(title="No data available").update_layout(**chart_theme)

        df = pd.DataFrame(list(data.items()), columns=['Asset', 'Amount'])
        fig = px.pie(
            df,
            values='Amount',
            names='Asset',
            color='Asset',
            color_discrete_sequence=asset_colors
        )
        
        fig.update_layout(
            **chart_theme,
            title={
                'text': "Current Investment Distribution",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        return fig

    @app.callback(
        Output('forecast-line-chart', 'figure'),
        Input('forecast-data', 'data')
    )
    def update_forecast_chart(data):
        if data is None:
            return go.Figure().update_layout(**chart_theme, title="No forecast data available")
        
        try:
            fig = go.Figure()
            
            if not all(key in data for key in ['years', 'asset_values', 'metadata']):
                return go.Figure().update_layout(**chart_theme, title="Invalid forecast data format")
            
            years = data['years']
            asset_values = data['asset_values']
            
            # Add traces for each asset class

                
            for i, (asset_class, values) in enumerate(asset_values.items()):
                color_idx = i % len(asset_colors)  # This will cycle through colors if there are more assets
                fig.add_trace(go.Scatter(
                    x=years,
                    y=values,
                    mode='lines',
                    name=asset_class,
                    line=dict(
                        color=asset_colors[color_idx]
                    )
                ))
            
            # Add total portfolio value
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
                    line=dict(
                        width=3,
                        dash='dash',
                        color='#00ff88'
                    )
                ))
            
            # Update layout with combined title
            title_text = (f"Portfolio Forecast over {data['metadata']['horizon']} Years<br>" +
                         f"<span style='font-size: 0.8em'>Inflation Rate: {data['metadata']['inflation_rate']*100:.1f}%</span>")
            
            fig.update_layout(
                **chart_theme,
                title={
                    'text': title_text,
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                xaxis_title="Years",
                yaxis_title="Value (Inflation-Adjusted $)",
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor="rgba(25, 25, 25, 0.9)",
                    bordercolor="rgba(255, 255, 255, 0.1)"
                )
            )
            
            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255, 255, 255, 0.1)'
            )
            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255, 255, 255, 0.1)'
            )
            
            return fig
        
        except Exception as e:
            print(f"Error in forecast chart callback: {e}")
            return go.Figure().update_layout(**chart_theme, title=f"Error creating forecast chart: {str(e)}")

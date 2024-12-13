from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import os
import json


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
        'paper_bgcolor': 'white',
        'plot_bgcolor': 'white',
        'font': {
            'family': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
            'color': '#888888'
        }
    }

    logout_button = html.Button(
        'Logout',
        id='logout-button',
        n_clicks=0,
        style={
            'position': 'absolute',
            'top': '20px',
            'right': '20px',
            'zIndex': 1000,  # Ensure it's on top of other content
            'cursor': 'pointer',
            'background': '#ff4a4a',  # Red logout button
            'color': 'white',
            'border': 'none',
            'borderRadius': '8px',
            'padding': '8px 16px'
        }
    )

    app.layout = html.Div(
        style={
            'background': 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
            'minHeight': '100vh',
            'padding': '2rem',
            'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
            'color': '#ffffff'
        },
        children=[
            logout_button,
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
            color_discrete_sequence=asset_colors,
            hole=0.4
        )
        
        fig.update_layout(
            **chart_theme,
            title={
                'text': "Future Investment Distribution",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': 'black'} 
            },
            legend={'font': {'color': 'black'}},  # Make legend text black
            showlegend=True
        )
        fig.update_traces(textinfo='percent+label')
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
            color_discrete_sequence=asset_colors,
            hole=0.4
        )
        
        fig.update_layout(
            **chart_theme,
            title={
                'text': "Current Investment Distribution",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': 'black'} 
            },
            legend={'font': {'color': 'black'}},  # Make legend text black
            showlegend=True
        )
        fig.update_traces(textinfo='percent+label')
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
            
            for i, (asset_class, values) in enumerate(asset_values.items()):
                color_idx = i % len(asset_colors)
                fig.add_trace(go.Scatter(
                    x=years,
                    y=values,
                    mode='lines+markers',  # Added markers
                    name=asset_class,
                    line=dict(
                        color=asset_colors[color_idx],
                        width=2
                    ),
                    marker=dict(
                        size=8,
                        color=asset_colors[color_idx]
                    )
                ))
            
            if asset_values:
                total_values = []
                for i in range(len(years)):
                    total = sum(values[i] for values in asset_values.values())
                    total_values.append(total)
                
                fig.add_trace(go.Scatter(
                    x=years,
                    y=total_values,
                    mode='lines+markers',
                    name='Total Portfolio Value',
                    line=dict(
                        width=3,
                        dash='dash',
                        color='#00ff88'
                    ),
                    marker=dict(
                        size=8,
                        color='#00ff88'
                    )
                ))
            
            title_text = (f"Portfolio Growth Projection")  # Simplified title
            
            fig.update_layout(
                **chart_theme,
                title={
                    'text': title_text,
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': 'black'}
                },
                xaxis_title="Years",
                yaxis_title="Value",
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor="white",
                    bordercolor='lightgray'
                ),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray',
                    gridwidth=1,
                    tickfont=dict(color='black')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray',
                    gridwidth=1,
                    tickfont=dict(color='black')
                )
            )
            
            return fig
        
        except Exception as e:
            print(f"Error in forecast chart callback: {e}")
            return go.Figure().update_layout(**chart_theme, title=f"Error creating forecast chart: {str(e)}")

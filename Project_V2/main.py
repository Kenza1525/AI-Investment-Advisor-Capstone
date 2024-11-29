import os
from dash import Dash
import dash_bootstrap_components as dbc
from flask import Flask
from auth_signup import main_layout


external_stylesheets = [dbc.themes.BOOTSTRAP]
external_scripts = [
    'http://localhost:8000/copilot/index.js',
    'https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.27.1/plotly.min.js'
]

server = Flask(__name__)
server.secret_key = os.urandom(24)

app = Dash(__name__,
            server=server, 
          external_stylesheets=external_stylesheets,
          external_scripts=external_scripts,
          suppress_callback_exceptions=True)

app.title = "Investment LLM"


if __name__ == "__main__":
    main_layout(app)
    app.run_server(debug=True)

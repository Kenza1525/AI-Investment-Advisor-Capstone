from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Initialize the app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Custom HTML template with all styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NexusWealth AI</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Righteous&display=swap');
            
            body {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                min-height: 100vh;
                margin: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .login-container {
                background: rgba(25, 25, 25, 0.9);
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 2rem;
                width: 100%;
                max-width: 400px;
            }
            .title {
                font-family: 'Righteous', cursive;
                font-size: 2.5rem;
                text-align: center;
                margin-bottom: 0.5rem;
                background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .subtitle {
                color: #888888;
                text-align: center;
                margin-bottom: 2rem;
                font-size: 1.1rem;
            }
            .input-group {
                margin-bottom: 1.5rem;
            }
            .custom-input {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #ffffff;
                padding: 12px 15px;
                width: 100%;
                transition: all 0.3s ease;
            }
            .custom-input:focus {
                outline: none;
                border-color: #00ff88;
                box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
            }
            .custom-input::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
            .button-container {
                display: flex;
                gap: 10px;
                justify-content: center;
            }
            .login-btn, .signup-btn {
                padding: 12px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
                border: none;
            }
            .login-btn {
                background: linear-gradient(90deg, #00ff88 0%, #00d4ff 100%);
                color: #1a1a1a;
            }
            .signup-btn {
                background: transparent;
                color: #00ff88;
                border: 2px solid #00ff88;
            }
            .login-btn:hover, .signup-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
            }
            .signup-btn:hover {
                background: rgba(0, 255, 136, 0.1);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the layout
app.layout = html.Div(
    className="d-flex justify-content-center align-items-center",
    style={"minHeight": "100vh"},
    children=[
        html.Div(
            className="login-container",
            children=[
                html.H1("NexusWealth AI", className="title"),
                html.P("Intelligent Investment Solutions", className="subtitle"),
                html.Div(
                    className="input-group",
                    children=[
                        dcc.Input(
                            type="text",
                            placeholder="Username",
                            className="custom-input"
                        )
                    ]
                ),
                html.Div(
                    className="input-group",
                    children=[
                        dcc.Input(
                            type="password",
                            placeholder="Password",
                            className="custom-input"
                        )
                    ]
                ),
                html.Div(
                    className="button-container",
                    children=[
                        html.Button(
                            "Login",
                            className="login-btn"
                        ),
                        html.Button(
                            "Sign Up",
                            className="signup-btn"
                        )
                    ]
                )
            ]
        )
    ]
)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
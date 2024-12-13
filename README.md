# AI-Investment-Advisor-Capstone
# ------------------------- Project Overview  ----------------------
This project is a custom-built Investment Advisory System designed to leverage Large Language Models (LLMs) and domain-specific tools to offer personalized financial advice, risk profiling, portfolio forecasting, and educational resources. The system integrates OpenAI's GPT model with LangChain, a retrieval-augmented generation (RAG) architecture, custom tools, and a Dash-powered interactive dashboard for visualization.

## Features
1. Personalized Investment Advice: Tailored investment recommendations based on user responses to a risk assessment questionnaire.
2. Portfolio Forecasting: Projects the growth of a user's investment portfolio over a specified time horizon.
3. Investment Education: Provides educational insights about the South African financial market.
4. Interactive Dashboard: Displays recommendations and portfolio forecasts using Dash for intuitive visualization.
6. Integration with LangChain: Ensures seamless handling of natural language queries and context-aware responses.
7. User Feedback Management: Collects and stores user feedback for improving system functionality.


# -----------------------System Architecture ------------------------
The project is composed of several tightly integrated components, as detailed below.

## Backend Components
1. Agent System: Defined in agent.py, it orchestrates the interaction between LLMs, tools, and user inputs using LangChain. Tools include:

2. Risk Profiling Tool (profile_tool.py) to assess a user's risk tolerance.
3. Personalized Advice Tool (personalised_advise_tool.py) for generating recommendations based on the risk profile.
4. Portfolio Forecaster (portfolio_forecast.py) for calculating growth projections.
5. Education Tool (education_tool.py) to provide domain-specific financial education.
6. APIs: The main.py serves as the entry point, managing API requests and interactions with the tools.

## Database Management
1. users_db.py: Handles user authentication and registration.
2. feedback_db.py: Logs and processes user feedback for system improvements.

## Frontend Components
1. Dash Dashboard (cmu-dash.py): Displays investment forecasts, risk profiles, and user-specific recommendations interactively.
2. clientside.js: Manages client-side events, including redirections and widget updates.
3. script2.js: Handles communication between the frontend and backend for updates like investment distributions and portfolio forecasts.

# --------------------- Installation and Setup ----------------------
## Prerequisites:
1. Python 3.8 or higher
2. Node.js (for frontend integration)
3. Access tokens for OpenAI and GitHub

## Clone the repository.
Run `git clone https://github.com/Kenza1525/AI-Investment-Advisor-Capstone.git` to clone the project into your local machine

## Install dependencies
Run `pip install -r requirements.txt` to install all the required software packages for this project.

## Set environment variables for API keys and access tokens in a .env file
OPENAI_API_KEY=your_openai_api_key
GITHUB_ACCESS_TOKEN=your_github_access_token
How to run the application:
1. `python main.py`
2. `python feedback.py`
3. `python3 -m chainlit run agent/agent.py -w -h`

# -------------------------How It Works ---------------------------------
## Risk Profiling

Users complete a questionnaire to determine their risk tolerance.
The RiskBasedAllocator in profile_tool.py calculates a risk score and allocates weights to asset classes.
Personalized Advice:

Using the PersonalizedAdviceTool, the system generates a recommended distribution of investment across asset classes.
Portfolio Forecasting:

The PortfolioForecaster projects portfolio growth over a time horizon, adjusting for inflation and asset-specific growth rates.
Investment Education:

The InvestmentEducationTool retrieves educational content from a GitHub repository, processed using FAISS for efficient search and retrieval.
Interactive Visualizations:

Dash displays investment distributions as pie charts and portfolio forecasts as line graphs.


## File Structure
1. agent/agent.py
2. cmu-dash_llm.py
3. main.py: Backend API manager
4. tools/profile_tool.py
5. tools/personalised_advise_tool.py
6. tools/portfolio_forecast.py
7. tools/education_tool.py
8. users_db.py
9. debug_db.py
10. feedback_db.py
11. assets/clientside.js
12. assets/script2.js
13. questions.py

# ---------------------- Future Work -----------------------
Expand educational content to include more global markets.
Introduce additional forecasting methods for higher accuracy.
Incorporate multi-language support for better accessibility.










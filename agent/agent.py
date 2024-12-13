from langchain_openai import OpenAI
from langchain.chains import LLMChain, APIChain
from langchain.memory.buffer import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
import chainlit as cl
import random
import chainlit.data as cl_data

from tools.profile_tool import RiskBasedAllocator
from questions import QUESTIONS
from tools.education_tool import InvestmentEducationTool 
from tools.portfolio_forecast import PortfolioForecaster
import matplotlib.pyplot as plt
import json
from datetime import datetime
from pathlib import Path

load_dotenv()
chat_history = []
investment_distribution = {}
distributionDone = False
user_profile = {}
profile_complete = False
growth_forecast = {}
forecast_ready = False
future_distribute = {}
future_distributeDone = False


feedback_fle = "feedback.jsonl"


ACCESS_TOKEN = "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"
investment_tool_instance = InvestmentEducationTool(
    repo= "Ayebilla/SA_Investment_info",
    access_token=ACCESS_TOKEN,
    api_key="sk-M2Zf8AteM_beMwQ9Q4yfCWNOIOuBf8XtGp4Mbh3Ib-T3BlbkFJ8s1Yat1knh6EdNcnmrqykaPopYeFM5AjEYyn0UyfgA"
)

@tool("InvestmentEducationTool", return_direct=False)
def investment_education_tool(query: str) -> dict:
    '''Provides educational information about the South African financial market.'''
    # Use the retriever tool to search for information
    retriever_tool = investment_tool_instance.get_tool()
    return retriever_tool({"query": query})


@tool("ProfileBasedTool", return_direct=False)
def personalized_advice_tool(risk_assessment_responses={'question1': 'a','question2': 'b','question3': 'c','question4': 'a','question5': 'b','question6': 'c','question7': 'd','question8': 'a','question9': 'b','question10': 'c','question11': 'd'}) -> dict:
    '''Returns a recommended distribution of an amount of money across asset classes based on the user's profile.
       Args: 
        - risk_assessment_responses: a dictionary containing the user's responses to the risk assessment questions.
        example: {
            'question1': 'a',
            'question2': 'b',
            'question3': 'c',
            'question4': 'a',
            'question5': 'b',
            'question6': 'c',
            'question7': 'd',
            'question8': 'a',
            'question9': 'b',
            'question10': 'c',
            'question11': 'd'
            }
        - amount: the amount of money the user wants to invest. Default is 5000.
    '''
    global investment_distribution, distributionDone
    user_risk = RiskBasedAllocator(risk_assessment_responses)
    investment_distribution = user_risk.risk_base_allocation()
    distributionDone = True
    return investment_distribution


@tool("PortfolioForecastTool", return_direct=False)
def forecast_portfolio_growth_tool(asset_distribution={"Local equity": 200,"Local bonds": 300,"Local cash": 100,"Global assets": 400}, horizon=10,inflation_rate=0.02):
    """
    Calculates the inflation-adjusted forecasted growth of a user's investment portfolio based on the recommended asset distribution.
    
    Args:
        - asset_distribution: A dictionary with asset classes as keys and allocated amounts as values.
        - time_horizon: The investment period in years.
        - inflation_rate: The annual inflation rate for adjusting portfolio growth.
    """
    global forecast_ready, growth_forecast
    forecaster = PortfolioForecaster(asset_distribution, horizon, inflation_rate)
    growth_forecast = forecaster.forecast_growth()
    if growth_forecast:
        forecast_ready = True
        #future_distributeDone = True
    return growth_forecast


class CustomDataLayer(cl_data.BaseDataLayer):

    async def upsert_feedback(self, feedback) -> str:
        global feedback_fle, latest_prompt

        # Dictionary to store new feedback
        new_feedback = {
            'id': feedback.forId,
            'user_prompt': latest_prompt,
            'feedback': feedback.comment,
            'value': feedback.value
        } 

        # print feedback 

        print(new_feedback)

        # Add new feedback
        with open(feedback_fle, "a") as file:

            file.write(json.dumps(new_feedback) + "\n")

    
    # Stub implementations

    async def build_debug_url(self, *args, **kwargs): pass
    async def create_element(self, element_dict): pass
    async def create_step(self, step_dict): pass
    async def create_user(self, user): pass
    async def delete_element(self, element_id): pass
    async def delete_feedback(self, feedback_id): pass
    async def delete_step(self, step_id): pass
    async def delete_thread(self, thread_id): pass
    async def get_element(self, thread_id, element_id): pass
    async def get_thread(self, thread_id): pass
    async def get_thread_author(self, thread_id): pass
    async def get_user(self, user_id): pass
    async def list_threads(self, pagination, filters): pass
    async def update_step(self, step_dict): pass
    async def update_thread(self, thread_id, name=None, user_id=None, metadata=None, tags=None): pass



# Chainlit setup
@cl.on_chat_start
def setup_chain():

    cl_data._data_layer = CustomDataLayer()

    llm = ChatOpenAI(openai_api_key="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", model="gpt-3.5-turbo")
    tools = [personalized_advice_tool,investment_education_tool, forecast_portfolio_growth_tool]
    llm_with_tools = llm.bind_tools(tools)
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
            "chat_history": lambda x: x["chat_history"]
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    cl.user_session.set("llm_chain", agent_executor)

# Prompt for the agent
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        '''
You are an investment advisor that helps users allocate their investment across a number of asset classes. 
You can provide either general investment advice or personalized advice based on the user's profile.A user can request for 
a forecast of their investment portfolio, educational information about the South African financial market, or general investment advice.

For portfolio forecasting:
If a user asks for a forecast of their investment portfolio, follow these exact steps:

First, check if there is an existing investment distribution. If not, inform the user that they need to get a personalized recommendation first.
If there is an investment distribution, ask the user for:

Time horizon (in years)
Inflation rate (as a decimal, e.g., 0.02 for 2%)
If they don't specify these, use default values of 10 years and 0.02 inflation rate.
You must use the forecast_portfolio_growth_tool for this task.
After getting the forecast results display them as a line chart in the dash app. 
Also explain to the user:
The growth projection for each asset class
The impact of inflation on their portfolio
The total projected value after the specified time period
Offer to run different scenarios with:

Different time horizons
Different inflation rates
Different initial investment amounts
You must ensure that the forecast is displayed as a line chart in the dash app if the forecast_ready flag is set to True.

Example interaction:
"I'll create a forecast using your current investment distribution:
[Show distribution]
The forecast has been generated and sent to the chart. You can see how each asset class is expected to grow over time.
Would you like to see how your portfolio might perform with different parameters? You can try:

A different time horizon (e.g., 5, 15, or 20 years)
Different inflation rates
Different investment amounts"


For educational information:
If a user asks for educational information about the South African financial market, you must use the `investment_education_tool` to provide relevant information.
The tool uses a retriever to search for information in a GitHub repository containing text files about the South African financial market and educational content on investment.
Also use investment_education_tool if the user asks for general advice. As much as possible, provide educational information about the South African financial market.  
If they ask for you to recommend some assets for them, you can ask if they want a personalized recommendation based on their profile or a general recommendation.


For personalized advice:
If a user asks for personalized advice, follow these exact steps:

First ask the user for the amount they want to invest.
Explain that you'll need to ask them 11 questions to assess their risk tolerance, and that they should respond with just the letter of their chosen option (a, b, c, or d).
Ask the questions ONE AT A TIME and wait for the user's response. As you collect responses, build a dictionary in this exact format:

"risk_assessment_responses = 
    'question1': '[user's letter response]',
    'question2': '[user's letter response]',
    'question3': '[user's letter response]',
    # ... and so on
"


After receiving each response, internally add it to your risk_assessment_responses dictionary and proceed to the next question.
After collecting all 11 responses, show the user their complete responses in this format:

Ask the user to confirm if these responses are correct. If they want to change any response, let them specify which question number they want to modify.
Once confirmed, use the completed risk_assessment_responses dictionary with the personalized_advice_tool like this:

risk_assessment_responses: a dictionary containing the user's responses to the risk assessment questions.
        "risk_assessment_responses=
            'question1': 'a',
            'question2': 'b',
            'question3': 'c',
            'question4': 'a',
            'question5': 'b',
            'question6': 'c',
            'question7': 'd',
            'question8': 'a',
            'question9': 'b',
            'question10': 'c',
            'question11': 'd'
            "
Before you begin asking the Questions 1 to 11, ask the user if they will like one of the pre-defined portfolios for retirees or recent graduates. If they do, ask them to specify the one they want and then proceed to offer the recommendations for that and do not proceed to ask the rest of the questions.
If a person is a retiree or recent graduate, you must use distributions given here:
Retiree portfolio - with the following distributions:
    Local equity: 20%
    Local bonds: 45%
    Local cash: 20%
    Global assets: 15%
Fresh Graduate portfolio - with the following distributions:
    Local equity: 10%
    Local bonds: 50%
    Local cash: 25%
    Global assets: 15%

Question 1: The principle objective of this investment is…
        options: 
            'a': To generate income
            'b': To preserve or guarantee investment capital
            'c': To achieve real returns (i.e. returns that beat inflation)
            'd': To achieve maximum capital growth
    
    Question 2: 'The investment term for this investment is…'
        options:
            'a': Less than 1 year
            'b': 1 to 3 years
            'c': 3 to 5 years
            'd': More than 5 years
    
    Question 3: 'I understand the effects of inflation. I prefer:'
        options:
            'a': To accept an appropriate level of risk as I require my investment to perform well ahead of inflation over time
            'b': To accept an appropriate level of risk as I require my investment to keep up with inflation over time
            'c': To preserve my capital at all costs even though this may mean returns are sometimes less than inflation
    

    Question 4: How important is it to you to achieve stable, consistent returns from this investment year in & year out?'
        'options':
            'a': Not very important, provided that the long-term outcome produces an above-average return that outpaces inflation
            'b': Reasonably important, but I can accept marginal variances in the value of my portfolio
            'c': Very important and I wish to avoid volatile swings in my fund values
    
    'Question 5':'What is the maximum capital loss that you would be willing to bear over the short-term if markets fell?'
        'options':
            'a': Above 20% - I am prepared to accept above average risk
            'b': 10% to 20% - I consider myself to be a moderate-risk investor
            'c': 0% to 10% - I consider myself to be a cautious investor'
            'd': I would really not like to face the possibility of a capital loss
        
    'Question 6': 'My first consideration when approaching this investment is:'
        'options':
            'a': I am willing to take more risk in order to beat inflation and obtain possible capital growth
            'b': I am committed to the investment term and believe that I have the discipline required
            'c': The level of risk is most important to me and I am willing to achieve more subdued returns
    
    'Question 7': 'When it comes to investing:'
        'options':
            'a': I invest in shares, make my own decisions on what to buy and sell
            'b': I fully understand financial matters but do not actively manage my investments
            'c': I consider my investment knowledge to be average
            'd': I consider my investment knowledge to be below average
    
    'Question 8': 'In times of excessive market volatility and fluctuation I:
        'options':
            'a': Am able to adhere to a long-term strategy
            'b': Am tempted to sell after a year if things have not recovered
            'c': Will sell if the underperformance prevails for more than six months
            'd': Am very concerned and am tempted to sell immediately
        
    'Question 9': 'Assuming an inflation rate of 6%, which outcome is most acceptable for R100,000 over five years?
        'options':
            'a': Best case: R250,000; worst case R80,000
            'b': Best case: R195,000; worst case R90,000
            'c': Best case: R140,000; worst case R100,000
    
    'Question 10': 'How dependent are you on the proceeds of this investment?'
        'options':
            'a': Not dependent at all; I can take risks that may lead to capital losses
            'b': Partially dependent; I can tolerate a marginal loss of 5-10%
            'c': Fairly dependent; I would not like to lose more than 5%
            'd': Totally dependent; I would not like to lose capital

    'Question 11': Would you accept risk to potentially enhance your return significantly
        'options':
            'a': I am prepared to take the chance and accept more risk than normal
            'b': I am prepared to accept higher risk with reasonable certainty of higher returns
            'c': I would be inclined to follow the safer route
            'd': I am unwilling to take on more risk than I have to

4. After gathering the profile information, display the user's answers as a dictionary for them to see and confirm or change their resposnes
5. Fill the risk_assessment dictionary in `personalized_advice_tool` and use it to recommend a distribution of the amount of money the user specify using the weights associated with each asset class from the 'Profpersonalized_advice_tool'.
6. Ensure that your recommendations are based on the asset classes returned from the `personalized_advice_tool`. Do not suggest any asset classes outside of what the tool returns.
7. Display the distribution as a pie chart in the dash app.
8. Show the user their risk tolerance level based on the responses they provided.

Always include a disclaimer to the user that the recommendations are based on the profile information they provided.

Ask for any missing information needed to complete the user's profile before providing personalized advice.

In the case of personalized advise ensure that the investment distribution is sent to the dash app to display as a pie chart. If there is any issue that prevents you from sending the distribution to be displayed as pie chart, report that.

Return a dictionary with the user's responses to be displayed as a pie chart in the dash app.
  
          '''
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

@cl.on_message
async def handle_message(message: cl.Message):
    global investment_distribution, distributionDone, user_profile, profile_complete,forecast_ready, growth_forecast, latest_prompt
    user_message = message.content.lower()

    latest_prompt = user_message

    llm_chain = cl.user_session.get("llm_chain")

    result = llm_chain.invoke({"input": user_message, "chat_history": chat_history})

    # If the result output is a dictionary, convert it to a formatted string
    if isinstance(result["output"], dict):
        output_content = json.dumps(result["output"], indent=2)  # Converting dict to a JSON formatted string
    else:
        output_content = result["output"]  # If it's already a string or list, keep it as is

    chat_history.extend([
        HumanMessage(content=user_message),
        AIMessage(content=output_content),  # Use the formatted string for AIMessage
    ])

    await cl.Message(output_content).send()

    if forecast_ready:
        # Ensure all keys in growth_forecast are strings
        growth_forecast = {str(k): v if isinstance(v, dict) else v for k, v in growth_forecast.items()}

        final_vals = {key: values[-1] for key, values in growth_forecast['asset_values'].items()}
        total_sum = sum(final_vals.values())
        future_distribute = {key: (values[-1]/total_sum)*360 for key, values in growth_forecast['asset_values'].items()}
        
        fn1 = cl.CopilotFunction(name="forecast-data", args=growth_forecast)
        fn2 = cl.CopilotFunction(name="future_investment_distribution", args=future_distribute)
        forecast_ready = False
        res = await fn1.acall()
        res = await fn2.acall()
        await cl.Message(content="Forecast and distribution information sent to the charts").send()


    if distributionDone:
        fn = cl.CopilotFunction(name="investment_distribution", args=investment_distribution)
        distributionDone = False
        res = await fn.acall()
        await cl.Message(content="Investment distribution sent to the chart").send()

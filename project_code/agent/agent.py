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

from tools.general_advise_tool import GeneralAdviceTool
from tools.personalised_advise_tool import PersonalizedAdviceTool
from tools.profile_tool import UserProfile
import matplotlib.pyplot as plt
import json

load_dotenv()
chat_history = []
investment_distribution = {}
distributionDone = False
user_profile = {}
profile_complete = False

@tool("GeneralAdviceTool", return_direct=False)
def general_advice_tool(sum_of_money: float = None, api_key: str = None) -> dict:
    '''Returns a recommended distribution of an amount of money across asset classes based on current market performance.'''
    general_tool = GeneralAdviceTool(api_key="KYpAilMplU1cVSK0H7N1P5OoR2znLbsIJa9yOER1")
    return general_tool.provide_advice(sum_of_money=sum_of_money)


@tool("PersonalizedAdviceTool", return_direct=False)
def personalized_advice_tool(profile_info: dict = None, sum_of_money: float = None, api_key: str = None) -> dict:
    '''Returns a recommended distribution of an amount of money across asset classes based on the user's profile.'''
    user = UserProfile(
        name=profile_info.get("Name"),
        age=profile_info.get("Age"),
        financial_goal=profile_info.get("Investment Goal"),
        investment_horizon=profile_info.get("Investment Length"),
        risk_tolerance=profile_info.get("Risk Tolerance Level")
    )
    
    personalized_tool = PersonalizedAdviceTool(api_key="KYpAilMplU1cVSK0H7N1P5OoR2znLbsIJa9yOER1")
    return personalized_tool.provide_advice(user_profile=user, sum_of_money=sum_of_money)

# Plot function for investment distribution
def plot_investment_distribution(investment_distribution):
    labels = investment_distribution.keys()
    sizes = investment_distribution.values()
    
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Investment Distribution')
    #plt.show()

# Chainlit setup
@cl.on_chat_start
def setup_chain():
    llm = ChatOpenAI(openai_api_key="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", model="gpt-3.5-turbo")
    tools = [general_advice_tool, personalized_advice_tool]
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
You can provide either general investment advice or personalized advice based on the user's profile.

For general advice:
If a user asks for general advice, you must use the `GeneralAdviceTool` to provide recommendations based on the current market performance. 
The market data is analyzed in the background using a MarketAnalysis algorithm. You should not ask for any profile information when the user requests general investment advice.

1. Use the `GeneralAdviceTool` to analyze the market and rank asset classes based on current performance.
2. Provide the recommendation to the user based on the best-performing asset classes.
3. If the user specifies an amount of money to invest, distribute it across the asset classes according to the rankings provided by the `GeneralAdviceTool`.
4. Inform the user that this allocation is based on current market performance data (e.g., price and percentage changes) sourced from Yahoo Finance.
5. Be sure to explain the ranking of asset classes to the user as returned by the `GeneralAdviceTool`.

For personalized advice:
If the user requests personalized advice, you must use the `PersonalizedAdviceTool` to tailor investment recommendations based on the user's specific profile information. 

1. Ask the user for the amount of money they have to invest and how many asset classes they would like to invest in (as in the general case).
2. Inform the user that you need to gather their profile information to provide personalized advice.
3. Gather the following information from the user:
   - Name
   - Age
   - Level of Education (Options: High School, Bachelor's, Master's, PhD, Other)
   - Investment Length (Options: Short-term, Medium-term, Long-term)
   - Investment Goal (Options: Retirement, Wealth Accumulation, Specific Purchase, Other)
   - Risk Tolerance Level (Options: Conservative, Moderate, Aggressive)
4. After gathering the profile information, use the `PersonalizedAdviceTool` to analyze the market and adjust the ranking of asset classes based on the user's risk tolerance, investment length, and goals.
5. Provide the recommendation to the user based on the best-performing asset classes and their profile.
6. Prioritize the asset classes based on the user's profile:
   - For example, if the user has a high risk tolerance, allocate a higher percentage of their investment to high-risk asset classes (e.g., stocks, cryptocurrencies).
7. If the user specifies an amount of money to invest, distribute it among the ranked asset classes according to the calculated weights, while considering the user's profile preferences.
8. Ensure that your recommendations are based on the asset classes returned from the `PersonalizedAdviceTool` (derived from the market analysis). Do not suggest any asset classes outside of what the tool returns.
   - You may recommend lower-performing asset classes if the user's profile suggests that they are suitable based on their risk tolerance and investment goals.

Always include a disclaimer to the user that the recommendations are based on the profile information they provided and current market data (average price and percentage changes) from Yahoo Finance.

Ask for any missing information needed to complete the user's profile before providing personalized advice.

In either case (general or personalized advice), ensure that the investment distribution is displayed to the user as a pie chart.
        '''
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

@cl.on_message
async def handle_message(message: cl.Message):
    global investment_distribution, distributionDone, user_profile, profile_complete

    user_message = message.content
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

    if distributionDone:
        fn = cl.CopilotFunction(name="investment_distribution", args=investment_distribution)
        distributionDone = False
        res = await fn.acall()
        await cl.Message(content="Investment distribution sent to the chart").send()

    if profile_complete:
        fn = cl.CopilotFunction(name="profile_update", args=user_profile)
        profile_complete = False
        res = await fn.acall()
        await cl.Message(content="Profile information sent to the form").send()
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
from questions import QUESTIONS

from tools.general_advise_tool import GeneralAdviceTool
#from tools.personalised_advise_tool import PersonalizedAdviceTool
from tools.profile_tool import RiskBasedAllocator
import matplotlib.pyplot as plt
import json

load_dotenv()
chat_history = []
investment_distribution = {}
distributionDone = False
user_profile = {}
profile_complete = False
question_mode = False
question_number = 1

@tool("GeneralAdviceTool", return_direct=False)
def general_advice_tool(sum_of_money: float = None, api_key: str = None) -> dict:
    '''Returns a recommended distribution of an amount of money across asset classes based on current market performance.'''
    global investment_distribution, distributionDone
    general_tool = GeneralAdviceTool(api_key="KYpAilMplU1cVSK0H7N1P5OoR2znLbsIJa9yOER1")
    investment_distribution = general_tool.provide_advice(sum_of_money=sum_of_money)
    distributionDone = True
    #return general_tool.provide_advice(sum_of_money=sum_of_money)
    return investment_distribution

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
    # user_risk = RiskBasedAllocator({
    #     'question1': risk_assessment_responses.get('question1'),
    #     'question2': risk_assessment_responses.get('question2'),
    #     'question3': risk_assessment_responses.get('question3'),
    #     'question4': risk_assessment_responses.get('question4'),
    #     'question5': risk_assessment_responses.get('question5'),
    #     'question6': risk_assessment_responses.get('question6'),
    #     'question7': risk_assessment_responses.get('question7'),
    #     'question8': risk_assessment_responses.get('question8'),
    #     'question9': risk_assessment_responses.get('question9'),
    #     'question10': risk_assessment_responses.get('question10'),
    #     'question11': risk_assessment_responses.get('question11')
    #     })
    global investment_distribution, distributionDone
    user_risk = RiskBasedAllocator(risk_assessment_responses)
    investment_distribution = user_risk.risk_base_allocation()
    distributionDone = True
    return investment_distribution

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
If a user asks for personalized advice, follow these exact steps:

First ask the user for the amount they want to invest.
Explain that you'll need to ask them 11 questions to assess their risk tolerance, and that they should respond with just the letter of their chosen option (a, b, c, or d).
Ask the questions ONE AT A TIME and wait for the user's response. As you collect responses, build a dictionary in this exact format:\

"risk_assessment_responses = 
    'question1': '[user's letter response]',
    'question2': '[user's letter response]',
    'question3': '[user's letter response]',
    # ... and so on
"


After receiving each response, internally add it to your risk_assessment_responses dictionary and proceed to the next question.
After collecting all 11 responses, show the user their complete responses in this format:

Ask the user to confirm if these responses are correct. If they want to change any response, let them specify which question number they want to modify.
Once confirmed, use the completed risk_assessment_responses dictionary with the ProfileBasedTool like this:

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
5. Fill the risk_assessment dictionary in `PersonalizedAdviceTool` and use it to recommend a distribution of the amount of money the user specify using the weights associated with each asset class from the 'PersonalizedAdviceTool'.
6. Ensure that your recommendations are based on the asset classes returned from the `PersonalizedAdviceTool`. Do not suggest any asset classes outside of what the tool returns.
7. Display the distribution as a pie chart in the dash app.

Always include a disclaimer to the user that the recommendations are based on the profile information they provided and current market data (average price and percentage changes) from Yahoo Finance.

Ask for any missing information needed to complete the user's profile before providing personalized advice.

In either case (general or personalized advice), ensure that the investment distribution is sent to the dash app to display as a pie chart. If there is any issue that prevents you from sending the distribution to be displayed as pie chart, report that.

Return a dictionary with the user's responses to be displayed as a pie chart in the dash app.
  
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

    print(investment_distribution)
    print(distributionDone)

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

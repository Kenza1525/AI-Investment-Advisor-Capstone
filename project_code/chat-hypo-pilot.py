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

load_dotenv()
chat_history = []
investment_distribution = {}
distributionDone = False
user_profile = {}
profile_complete = False

@tool("InvestmentTool", return_direct=False)
def InvestmentTool(sum_of_money: float = None, number_of_stocks: int = None) -> dict:
    """
    Use this tool to advise the user on how to allocate their money into a given number of stocks.
    You need to provide two parameters: sum_of_money (the total amount to invest) and number_of_stocks (the number of stocks to invest in).
    The tool will return a dictionary with a random percentage distribution across the given number of stocks.
    """
    global investment_distribution, distributionDone

    if sum_of_money is None or number_of_stocks is None:
        return "Please provide both the sum of money to invest and the number of stocks to invest in."

    if number_of_stocks < 1 or number_of_stocks > 5:
        return "The number of stocks must be between 1 and 5."

    percentages = [random.random() for _ in range(number_of_stocks)]
    total_percentage = sum(percentages)
    percentages = [p / total_percentage for p in percentages]

    investment_options = ["Apple stock", "Microsof stock", "Nvidia stock", "MTN Rwanda stock", "Tesla stock"]
    selected_options = investment_options[:number_of_stocks]
    
    investment_distribution = {option: round(sum_of_money * p, 2) for option, p in zip(selected_options, percentages)}
    distributionDone = True
    
    return investment_distribution

@tool("ProfileTool", return_direct=False)
def ProfileTool(profile_info: dict = None) -> dict:
    """
    Use this tool to gather and update the user's profile information for personalized investment advice.
    The profile information includes: name, email, age, education, investment length, investment goal, risk tolerance, investment knowledge, financial class, and employment status.
    """
    global user_profile, profile_complete
    if profile_info:
        user_profile.update(profile_info)
        if all(user_profile.values()):
            profile_complete = True
    return user_profile

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        '''
You are an investment advisor that helps users allocate their investment across a number of investment options.
You can provide general investment advice or personalized advice based on the user's profile.
Here are the list of investment options you can select from:
1. Stocks/Equities
2. Bonds
3. Mutual Funds
4. Exchange-Traded Funds (ETFs)
5. Real Estate
6. Certificates of Deposit (CDs)
7. Retirement Accounts 
8. Commodities
9. Cryptocurrencies
10. Savings Accounts
11. Hedge Funds
12. Venture Capital/Private Equity
13. Annuities
14. Options and Derivatives

For general advice:
1. Determine the sum of money and the number of stocks the user wants to invest in.
2. Use the InvestmentTool to calculate the percentage distribution of the sum across the investment options.
3. Provide the recommendation to the user.

For personalized advice:
1. Ask the user of the amount of money they have to invest and number of stocks they will like to invest in just as in the general case 
Inform the user that you need to gather their profile information for personalized advice.
2. Use the ProfileTool to gather the following information:
   - Name
   - Age
   - Level of Education (Options: High School, Bachelor's, Master's, PhD, Other)
   - Investment Length (Options: Short-term, Medium-term, Long-term)
   - Investment Goal (Options: Retirement, Wealth Accumulation, Specific Purchase, Other)
   - Risk Tolerance Level (Options: Low, Medium, High)
3. After gathering the profile and the amount of money and number of investment options, use your best guess to recommend a distribution of their money to the number of options. Your remcommedations must be within the investments listed here. 
Do not recommend anything outside of the investment otpions provided. You're free to use your own judgement and knowledge of those investments to do the recommendation in whatever way you see fit.
  - Explain to the user that the recommendation is based on the information they provided and that it is important for them to further research and consult with a financial advisor before making any investment decisions.
  If for example a young under 30 years old person with a high risk tolerance wants to invest in 5 options, you might recommend a higher percentage of their money in high-risk investment options.
  In terms of risk, use your best judgement to rank the available investment options from low to high risk.
The user profile information will be sent to a form for further processing. They might come in different order and you should be able to handle that.Ask for any missing information to be able to send the profile information to the form.
Always ask for clarification if any information is missing or unclear.
        '''
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

@cl.on_chat_start
def setup_chain():
    llm = ChatOpenAI(openai_api_key="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", model="gpt-3.5-turbo")
    tools = [InvestmentTool, ProfileTool]
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

@cl.on_message
async def handle_message(message: cl.Message):
    global investment_distribution, distributionDone, user_profile, profile_complete

    user_message = message.content
    llm_chain = cl.user_session.get("llm_chain")

    result = llm_chain.invoke({"input": user_message, "chat_history": chat_history})
    chat_history.extend([
        HumanMessage(content=user_message),
        AIMessage(content=result["output"]),
    ])

    await cl.Message(result['output']).send()

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
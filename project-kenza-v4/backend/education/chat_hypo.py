from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain_core.messages import AIMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from langchain_core.tools import tool
import os
import glob
from backend.config.config import Config
from backend.asset_allocation.questions import QUESTIONS, RISK_PROFILES
import chainlit as cl

# Global variables for storing user information and investment details
user_info = {
    "fullName": "",
    "job": "",
    "age": "",
    "phoneNumber": "",
    "email": ""
}

investment_details = {
    "amount": 0,
    "time_horizon": 0,
    "allocation": None
}

class PortfolioForecaster:
    def __init__(self, initial_allocations, horizon, inflation_rate=0.02):
        self.initial_allocations = initial_allocations
        self.time_horizon = horizon
        self.inflation_rate = inflation_rate
        self.growth_rates = {
            "Local equity": 0.10,
            "Local bonds": 0.05,
            "Local cash": 0.00,
            "Global assets": 0.07
        }
    
    def forecast_growth(self):
        forecast = {str(year): {} for year in range(self.time_horizon + 1)}
        
        for asset_class, initial_amount in self.initial_allocations.items():
            growth_rate = self.growth_rates.get(asset_class, 0.0)
            current_value = initial_amount
            for year in range(self.time_horizon + 1):
                current_value = current_value * (1 + growth_rate) / (1 + self.inflation_rate)
                forecast[str(year)][asset_class] = current_value
        
        return {
            "years": list(map(str, range(self.time_horizon + 1))),
            "asset_values": {
                asset_class: [forecast[str(year)][asset_class] 
                            for year in range(self.time_horizon + 1)]
                for asset_class in self.initial_allocations.keys()
            },
            "metadata": {
                "horizon": self.time_horizon,
                "inflation_rate": self.inflation_rate
            }
        }

@tool("education_tool")
async def education_tool(query: str) -> str:
    """Tool for providing investment education and information about markets."""
    try:
        education_agent = cl.user_session.get("education_agent")
        if education_agent is None:
            return "Education system is not properly initialized. Please try again."
        return await education_agent.retriever_tool.arun(query)  # Made async
    
    except Exception as e:
        print(f"Education tool error: {str(e)}")
        return "Error retrieving educational information"

@tool("asset_allocation_tool")
def asset_allocation_tool(action: str, data: dict = None) -> str:
    """
    Tool for handling asset allocation questionnaire and profile determination.
    Actions: check_prerequisites, store_personal_info, process_answer, calculate_profile
    """
    global user_info
    
    if action == "check_prerequisites":
        return all(value != "" for value in user_info.values())
    
    elif action == "store_personal_info":
        if not data:
            return "Please provide personal information"
        user_info.update(data)
        # Send to frontend
        cl.CopilotFunction(name="update_personal_info", args=user_info).send()
        return "Personal information stored"
    
    elif action == "calculate_profile":
        score = data.get("score", 0)
        for (min_score, max_score), (profile, allocation) in RISK_PROFILES.items():
            if min_score <= score <= max_score:
                investment_details["allocation"] = allocation
                # Send to frontend
                cl.CopilotFunction(
                    name="update_allocation_chart",
                    args={"profile": profile, "allocation": allocation, "score": score}
                ).send()
                return f"Profile calculated: {profile}"
    
    return "Invalid action for asset allocation tool"

@tool("forecasting_tool")
def forecasting_tool(amount: float, horizon: int) -> str:
    """Tool for forecasting portfolio growth based on asset allocation."""
    global investment_details
    
    if not investment_details["allocation"]:
        return "Please complete asset allocation questionnaire first"
    
    investment_details["amount"] = amount
    investment_details["time_horizon"] = horizon
    
    # Calculate initial amounts for each asset class
    initial_allocations = {
        asset: (percentage / 100) * amount
        for asset, percentage in investment_details["allocation"].items()
    }
    
    # Generate forecast
    forecaster = PortfolioForecaster(initial_allocations, horizon)
    forecast_data = forecaster.forecast_growth()
    
    # Send forecasting charts to frontend
    cl.CopilotFunction(
        name="update_forecast_charts",
        args={
            "lineChart": forecast_data,
            "finalPieChart": {
                asset: values[-1] 
                for asset, values in forecast_data["asset_values"].items()
            }
        }
    ).acall()
    
    return "Forecast generated successfully"

class FinancialAgent:
    def __init__(self):
        self.llm = ChatOpenAI(api_key=Config.OPENAI_API_KEY, model="gpt-3.5-turbo")
        self.embeddings = OpenAIEmbeddings(api_key=Config.OPENAI_API_KEY)
        self.chat_history = []
        self.setup_knowledge_base()
        self.setup_agent()

    def setup_knowledge_base(self):
        data_path = os.path.join(os.path.dirname(__file__), 'data', '*.txt')
        all_files = glob.glob(data_path)
        
        if not all_files:
            raise Exception("No education data files found")
        
        combined_text = ""
        for file_path in all_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                combined_text += f.read() + "\n\n"

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(combined_text)
        self.vector_store = FAISS.from_texts(texts, self.embeddings)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        self.retriever_tool = create_retriever_tool(
            self.retriever,
            "investment_knowledge",
            "Search for information about investments, markets, and investment concepts."
        )

    def setup_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a comprehensive financial advisor with expertise in:

1. Investment Education:
- Investment Basics (stocks, bonds, mutual funds, ETFs)
- Risk Management (portfolio diversification, risk assessment)
- Market Analysis (trends, analysis techniques)

2. Asset Allocation:
- Personal information must be collected first
- Risk profiling through questionnaire
- Portfolio distribution based on risk profile

3. Portfolio Forecasting:
- Requires investment amount and time horizon
- Uses asset allocation data for predictions
- Projects growth for different asset classes

Use the appropriate tool based on the user's needs. For asset allocation and forecasting, ensure personal information is collected first.
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        tools = [education_tool, asset_allocation_tool, forecasting_tool]
        llm_with_tools = self.llm.bind_tools(tools)

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

        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    async def run(self, message: str):
        try:
            result = await self.agent_executor.ainvoke({
                "input": message,
                "chat_history": self.chat_history
            })
            
            self.chat_history.extend([
                HumanMessage(content=message),
                AIMessage(content=result["output"]),
            ])
            
            return result["output"]
        except Exception as e:
            print(f"Error in run method: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."

async def setup_agent():
    try:
        agent = FinancialAgent()
        # Store the agent in the user session
        cl.user_session.set("education_agent", agent)
        return agent
    except Exception as e:
        print(f"Error setting up agent: {str(e)}")
        return None

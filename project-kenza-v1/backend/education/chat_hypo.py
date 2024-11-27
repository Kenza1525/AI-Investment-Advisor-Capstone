from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Fixed import
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain_core.messages import AIMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
import os
import glob
from backend.config.config import Config
import chainlit as cl

class EducationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model="gpt-3.5-turbo"
        )
        self.embeddings = OpenAIEmbeddings(
            api_key=Config.OPENAI_API_KEY
        )
        self.chat_history = []
        self.setup_knowledge_base()
        self.setup_agent()

    def setup_knowledge_base(self):
        # Load documents from data directory and prepare retriever tool
        data_path = os.path.join(os.path.dirname(__file__), 'data', '*.txt')
        all_files = glob.glob(data_path)
        
        combined_text = ""
        for file_path in all_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                combined_text += f.read() + "\n\n"

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        texts = text_splitter.split_text(combined_text)
        self.vector_store = FAISS.from_texts(texts, self.embeddings)
        
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 3}
        )
        self.retriever_tool = create_retriever_tool(
            self.retriever,
            "investment_knowledge",
            "Search for information about investments, JSE markets, and South African investment concepts."
        )

    def setup_agent(self):
        # Setup the agent with the appropriate tools and prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a sophisticated investment education assistant specializing in South African markets. 
            Your role is to educate users about investment concepts, the JSE, and investment strategies."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        tools = [self.retriever_tool]
        llm_with_tools = self.llm.bind_tools(tools)

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"]
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )

        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    async def run(self, message: str):
        """Run method for the agent"""
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
            return f"I apologize, but I encountered an error: {str(e)}"

    async def formfill(self, **form_data):
        """Function to handle form filling on the dashboard"""
        return form_data

    async def update_chart(self, profile_data: dict):
        """Function to handle chart updates on the dashboard"""
        return profile_data


@cl.on_chat_start
def setup_education_agent():
    cl.user_session.set("education_agent", EducationAgent())


@cl.on_message
async def handle_message(message: cl.Message):
    user_message = message.content.lower()
    education_agent = cl.user_session.get("education_agent")
    result = await education_agent.run(user_message)
    await cl.Message(result).send()

    # Triggering formfill or update_chart function if needed
    if "form fields" in result:
        form_data = {
            "fullName": "keriane",
            "job": "student",
            "age": 27,
            "phoneNumber": "0789362895",
            "email": "xy@gamil.com"
        }
        await handle_chainlit_fn_call("formfill", form_data)

    if "allocation" in result:
        chart_data = {
            "profile": "Moderate",
            "allocation": {"Local equity": 20, "Local bonds": 45, "Local cash": 20, "Global assets": 15}
        }
        await handle_chainlit_fn_call("update_chart", chart_data)


async def handle_chainlit_fn_call(fn_name, data):
    """Manually handle chainlit function calls and simulate callbacks"""
    # You can simulate a call back to JavaScript if needed
    if fn_name == "formfill":
        await cl.emit("chainlit-call-fn", {"name": "formfill", "args": data})
    elif fn_name == "update_chart":
        await cl.emit("chainlit-call-fn", {"name": "update_chart", "args": data})


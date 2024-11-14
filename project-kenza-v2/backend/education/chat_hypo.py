from langchain_openai import ChatOpenAI, OpenAIEmbeddings
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
        try:
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
        except Exception as e:
            print(f"Error initializing EducationAgent: {str(e)}")
            raise

    def setup_knowledge_base(self):
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'data', '*.txt')
            all_files = glob.glob(data_path)
            
            if not all_files:
                raise Exception("No education data files found")
            
            combined_text = ""
            for file_path in all_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_text += f.read() + "\n\n"

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,  # Default if not in Config
                chunk_overlap=200  # Default if not in Config
            )
            texts = text_splitter.split_text(combined_text)
            self.vector_store = FAISS.from_texts(texts, self.embeddings)
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            self.retriever_tool = create_retriever_tool(
                self.retriever,
                "investment_knowledge",
                "Search for information about investments, JSE markets, and South African investment concepts."
            )
        except Exception as e:
            print(f"Error in setup_knowledge_base: {str(e)}")
            raise

    def setup_agent(self):
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a sophisticated investment education assistant specializing in South African markets. 
                Use the retrieved information to provide clear, accurate answers about investment concepts, the JSE, and investment strategies.
                If you don't find specific information in the retrieved documents, say so and provide general investment guidance."""),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])

            tools = [self.retriever_tool]
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
        except Exception as e:
            print(f"Error in setup_agent: {str(e)}")
            raise

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
            print(f"Error in run method: {str(e)}")
            return "I apologize, but I encountered an error while processing your question. Please try asking in a different way or ask another question."

async def setup_education_agent():
    """Initialize and return the education agent"""
    try:
        agent = EducationAgent()
        return agent
    except Exception as e:
        print(f"Error setting up education agent: {str(e)}")
        return None
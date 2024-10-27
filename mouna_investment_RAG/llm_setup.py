import os
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool

def initialize_llm(api_key):
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)
    return llm

def setup_tools(vector_store):
    retriever = vector_store.as_retriever()
    retriever_tool = create_retriever_tool(
        retriever,
        "investment_search",
        "Useful for searching financial data and market information..."
    )
    return retriever_tool
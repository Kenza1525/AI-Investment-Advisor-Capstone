from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from questions import RISK_PROFILES, QUESTIONS
import config  # Import the entire config module

class AssetAllocationAdvisor:
    def __init__(self):
        # No need to set environment variables here as they're set in config.py
        self.llm = ChatOpenAI(
            api_key=config.OPENAI_API_KEY,
            temperature=0
        )
        self.embeddings = OpenAIEmbeddings(
            api_key=config.OPENAI_API_KEY
        )
        self.setup_knowledge_base()
        self.setup_prompt_template()

    def setup_knowledge_base(self):
        knowledge_text = """
        Investment Risk Profile System

        The system evaluates investors through a questionnaire covering:
        1. Primary investment objective
        2. Investment term
        3. Risk tolerance

        Risk Profiles and Asset Allocations:

        1. Conservative (Score 20-30):
        - For investors seeking current income and stability
        - Asset Allocation:
          * Local equity: 10%
          * Local bonds: 50%
          * Local cash: 25%
          * Global assets: 15%

        2. Cautious (Score 31-45):
        - For investors prioritizing capital protection over growth
        - Asset Allocation:
          * Local equity: 15%
          * Local bonds: 50%
          * Local cash: 20%
          * Global assets: 15%

        3. Moderate (Score 46-65):
        - For investors seeking real growth with acceptable volatility
        - Asset Allocation:
          * Local equity: 20%
          * Local bonds: 45%
          * Local cash: 20%
          * Global assets: 15%

        4. Aggressive (Score 66-77):
        - For investors seeking maximum growth with higher risk tolerance
        - Asset Allocation:
          * Local equity: 25%
          * Local bonds: 45%
          * Local cash: 15%
          * Global assets: 15%
        """

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(knowledge_text)
        self.vector_store = FAISS.from_texts(texts, self.embeddings)

    def setup_prompt_template(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an investment advisor specializing in risk profiling and asset allocation.
            Your role is to help explain the risk profiling process and asset allocation strategies.
            
            Key Guidelines:
            - Provide clear, concise explanations about the risk profiling process
            - Explain how scores translate to risk profiles
            - Detail how asset allocation is determined for each risk profile
            - Use specific percentages and numbers from the knowledge base
            - Be direct and professional in your responses"""),
            ("human", "{question}"),
            ("human", "Please provide a clear and specific answer based on the available information.")
        ])

    def get_response(self, question):
        docs = self.vector_store.similarity_search(question)
        context = "\n".join([doc.page_content for doc in docs])
        
        chain = self.prompt | self.llm
        response = chain.invoke({"question": f"Context: {context}\n\nQuestion: {question}"})
        
        return response.content
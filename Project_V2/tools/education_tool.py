# from langchain_community.vectorstores import FAISS
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.document_loaders import GithubFileLoader
# from langchain_openai import OpenAIEmbeddings
# from langchain.tools.retriever import create_retriever_tool


# ACCESS_TOKEN = "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"
# loader = GithubFileLoader(
#     repo="Ayebilla/cmu_capstone",
#     access_token=ACCESS_TOKEN,
#     github_api_url="https://api.github.com",
#     file_filter=lambda file_path: file_path.endswith("txt"),
# )
# documents = loader.load()

# embeddings = OpenAIEmbeddings()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
# documents = text_splitter.split_documents(documents)
# vector = FAISS.from_documents(documents, embeddings)

# retriever = vector.as_retriever()
# retriever_tool = create_retriever_tool(
#     retriever,
#     "investment_search",
#     "Useful for providing financial education especially about the South African financial market"
#     "Search for information about South African financial market. For any search related to investment education or South African market, you must use this tool!",
# )


# from langchain_community.vectorstores import FAISS
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain.document_loaders import GithubFileLoader
# from langchain_community.document_loaders import GithubFileLoader
# from langchain_openai import OpenAIEmbeddings
# from langchain.tools.retriever import create_retriever_tool


# class InvestmentEducationTool:
#     def __init__(self, repo: str, access_token: str, chunk_size: int = 100, chunk_overlap: int = 20):
#         self.repo = repo
#         self.access_token = access_token
#         self.chunk_size = chunk_size
#         self.chunk_overlap = chunk_overlap

#         # Load documents from GitHub repository
#         self.documents = self._load_documents()

#         # Initialize embeddings and vector store

#         api_key = 'sk-M2Zf8AteM_beMwQ9Q4yfCWNOIOuBf8XtGp4Mbh3Ib-T3BlbkFJ8s1Yat1knh6EdNcnmrqykaPopYeFM5AjEYyn0UyfgA'
     
#         self.embeddings = OpenAIEmbeddings()
#         self.vector = self._create_vector_store(api_key)

#         # Create retriever and tool
#         self.retriever = self.vector.as_retriever()
#         self.retriever_tool = self._create_retriever_tool()

#     def _load_documents(self):
#         # Load text files from the specified GitHub repository
#         loader = GithubFileLoader(
#             repo=self.repo,
#             access_token=self.access_token,
#             github_api_url="https://api.github.com",
#             file_filter=lambda file_path: file_path.endswith("txt"),
#         )
#         return loader.load()

#     def _create_vector_store(self):
#         # Split documents into smaller chunks and create FAISS vector store
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=self.chunk_size,
#             chunk_overlap=self.chunk_overlap
#         )
#         documents = text_splitter.split_documents(self.documents)
#         return FAISS.from_documents(documents, self.embeddings)

#     def _create_retriever_tool(self):
#         # Create retriever tool for the investment education context
#         return create_retriever_tool(
#             self.retriever,
#             "investment_search",
#             "Useful for providing financial education, especially about the South African financial market. "
#             "Search for information about the South African financial market. For any search related to investment education or South African market, you must use this tool!"
#         )

#     def get_tool(self):
#         # Returns the retriever tool for external use
#         return self.retriever_tool


from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GithubFileLoader
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

class InvestmentEducationTool:
    def __init__(self, repo: str, access_token: str, api_key: str, chunk_size: int = 100, chunk_overlap: int = 20):
        api_key = 'sk-M2Zf8AteM_beMwQ9Q4yfCWNOIOuBf8XtGp4Mbh3Ib-T3BlbkFJ8s1Yat1knh6EdNcnmrqykaPopYeFM5AjEYyn0UyfgA'
        self.repo = repo
        self.access_token = access_token
        self.api_key = api_key
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Load documents from GitHub repository
        self.documents = self._load_documents()

        # Initialize embeddings and vector store
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.vector = self._create_vector_store()

        # Create retriever and tool
        self.retriever = self.vector.as_retriever()
        self.retriever_tool = self._create_retriever_tool()

    def _load_documents(self):
        # Load text files from the specified GitHub repository
        loader = GithubFileLoader(
            repo=self.repo,
            access_token=self.access_token,
            github_api_url="https://api.github.com",
            file_filter=lambda file_path: file_path.endswith("txt"),
        )
        return loader.load()

    def _create_vector_store(self):
        # Split documents into smaller chunks and create FAISS vector store
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        documents = text_splitter.split_documents(self.documents)
        return FAISS.from_documents(documents, self.embeddings)

    def _create_retriever_tool(self):
        # Create retriever tool for the investment education context
        return create_retriever_tool(
            self.retriever,
            "investment_search",
            "Useful for providing financial education, especially about the South African financial market. "
            "Search for information about the South African financial market. For any search related to investment education or South African market, you must use this tool!"
        )

    def get_tool(self):
        # Returns the retriever tool for external use
        return self.retriever_tool

from web_scraping import save_investment_content, save_file
from text_processing import split_text
from vector_store import create_vector_store
from llm_setup import initialize_llm, setup_tools
from agent_setup import create_agent

# Load and save investment content
links = [
    "https://www.jse.co.za/",
    "https://www.jse.co.za/learn-how-to-invest/what-are-shares",
    "https://www.jse.co.za/learn-how-to-invest/why-invest-shares",
    "https://www.jse.co.za/learn-how-to-invest/what-are-dividends",
    "https://www.jse.co.za/learn-how-to-invest/what-are-derivatives",
    "https://www.jse.co.za/learn-how-to-invest/what-are-options",
    "https://www.jse.co.za/learn-how-to-invest/what-interest",
    "https://www.jse.co.za/learn-how-to-invest/what-are-bonds",
    "https://www.jse.co.za/learn-how-to-invest/types-bonds",
    "https://www.jse.co.za/learn-how-to-invest/what-are-futures",
    "https://www.jse.co.za/learn-how-to-invest/what-are-commodities",
    "https://www.jse.co.za/learn-how-to-invest/what-are-returns",
    "https://www.jse.co.za/learn-how-to-invest/currency-derivatives-forex",
    "https://www.jse.co.za/learn-how-to-invest/exchange-traded-funds-etfs",
    "https://www.jse.co.za/learn-how-to-invest/warrants",
    "https://www.jse.co.za/learn-how-to-invest/technical-analysis-fundamentals",
    "https://www.jse.co.za/learn-how-to-invest/technical-analysis-trendlines",
    "https://www.jse.co.za/learn-how-to-invest/itac",
    "https://www.jse.co.za/learn-how-to-invest/commodities-influencers-forwards",
    "https://www.jse.co.za/learn-how-to-invest/bonds-determining-interest-yields",
    "https://www.jse.co.za/learn-how-to-invest/accessing-market/different-ways-invest",
    "https://www.jse.co.za/learn-how-to-invest/accessing-market/who-invest-and-where-find-them",
    "https://www.jse.co.za/learn-how-to-invest/accessing-market/functions-exchange",
    "https://www.jse.co.za/learn-how-to-invest/accessing-market/trading-vs-investing",
    "https://www.jse.co.za/learn-how-to-invest/accessing-market/jse-financial-markets",
    "https://www.jse.co.za/learn-how-to-invest/accessing-market/share-indices",
    "https://www.jse.co.za/learn-how-to-invest/accessing-market/market-capitalisation",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/wealth-creation-process",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/mind-investor",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/are-you-ready-invest",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/things-consider-when-investing",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/what-it-means-be-investor",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/determining-value-company",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/how-read-financial-results",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/tax-implications-linked-investing",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/dividends-capital-growth",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/compiling-your-investment-portfolio",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/taxfree-and-microinvesting",
    "https://www.jse.co.za/learn-how-to-invest/being-investor/managing-risk-linked-investing"
]

# Save content from the provided links
contents = [save_investment_content(link, save_file) for link in links]
content_combined = "".join(contents)
save_file("investment_content.txt", content_combined)

# Process and split text
documents_split = split_text("investment_content.txt")

# Create vector store
api_key = 'sk-M2Zf8AteM_beMwQ9Q4yfCWNOIOuBf8XtGp4Mbh3Ib-T3BlbkFJ8s1Yat1knh6EdNcnmrqykaPopYeFM5AjEYyn0UyfgA'
vector_store = create_vector_store(documents_split, api_key)

# Initialize LLM and tools
llm = initialize_llm(api_key)
retriever_tool = setup_tools(vector_store)
tools = [retriever_tool]

# Create and execute agent
agent_executor = create_agent(llm, tools)

# Example query
query = "What is JSE?"
result = agent_executor.invoke({"input": query, "chat_history": []})
print(result["output"])

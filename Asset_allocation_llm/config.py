import os

# Set environment variables for the API keys
os.environ["OPENAI_API_KEY"] = 'sk-M2Zf8AteM_beMwQ9Q4yfCWNOIOuBf8XtGp4Mbh3Ib-T3BlbkFJ8s1Yat1knh6EdNcnmrqykaPopYeFM5AjEYyn0UyfgA'
os.environ["LANGCHAIN_API_KEY"] = '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'

# Export the keys as variables
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
LANGCHAIN_API_KEY = os.environ["LANGCHAIN_API_KEY"]
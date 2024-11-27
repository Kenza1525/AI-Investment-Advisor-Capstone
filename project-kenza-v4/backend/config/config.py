import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-M2Zf8AteM_beMwQ9Q4yfCWNOIOuBf8XtGp4Mbh3Ib-T3BlbkFJ8s1Yat1knh6EdNcnmrqykaPopYeFM5AjEYyn0UyfgA')
    LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', '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')

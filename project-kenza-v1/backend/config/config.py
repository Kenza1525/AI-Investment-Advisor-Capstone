import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-M2Zf8AteM_beMwQ9Q4yfCWNOIOuBf8XtGp4Mbh3Ib-T3BlbkFJ8s1Yat1knh6EdNcnmrqykaPopYeFM5AjEYyn0UyfgA')
    LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', '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')
    
    # Server Configuration
    CHAINLIT_SERVER = "http://localhost:8000"
    DASH_SERVER = "http://localhost:8050"
    
    # RAG Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Asset Allocation Configuration
    RISK_PROFILES = {
        (20, 30): ('Conservative', {
            'Local equity': 10,
            'Local bonds': 50,
            'Local cash': 25,
            'Global assets': 15
        }),
        (31, 45): ('Cautious', {
            'Local equity': 15,
            'Local bonds': 50,
            'Local cash': 20,
            'Global assets': 15
        }),
        (46, 65): ('Moderate', {
            'Local equity': 20,
            'Local bonds': 45,
            'Local cash': 20,
            'Global assets': 15
        }),
        (66, 77): ('Aggressive', {
            'Local equity': 25,
            'Local bonds': 45,
            'Local cash': 15,
            'Global assets': 15
        })
    }
    
    # Form Fields Configuration
    PERSONAL_INFO_FIELDS = [
        'fullName',
        'job',
        'age',
        'phoneNumber',
        'email'
    ]
    
    @staticmethod
    def validate_config():
        """Validate that all required configuration is present"""
        required_vars = ['OPENAI_API_KEY', 'LANGCHAIN_API_KEY']
        for var in required_vars:
            if not getattr(Config, var):
                raise ValueError(f"Missing required configuration: {var}")
        return True

    @staticmethod
    def get_risk_profile_ranges():
        """Get risk profile score ranges"""
        return list(Config.RISK_PROFILES.keys())

    @staticmethod
    def get_risk_profile(score):
        """Get risk profile based on score"""
        for (min_score, max_score), (profile, allocation) in Config.RISK_PROFILES.items():
            if min_score <= score <= max_score:
                return profile, allocation
        return None, None
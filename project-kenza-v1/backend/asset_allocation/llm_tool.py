from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Dict, Any
from backend.config.config import Config

class AssetAllocationAdvisor:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model="gpt-3.5-turbo"
        )
        self.setup_prompt_templates()
        self.risk_profiles = {
            'Conservative': {
                'score_range': (20, 30),
                'allocation': {
                    'Local equity': 10,
                    'Local bonds': 50,
                    'Local cash': 25,
                    'Global assets': 15
                },
                'description': ('Suitable for investors who prioritize capital preservation '
                              'and are sensitive to market volatility.')
            },
            'Cautious': {
                'score_range': (31, 45),
                'allocation': {
                    'Local equity': 15,
                    'Local bonds': 50,
                    'Local cash': 20,
                    'Global assets': 15
                },
                'description': ('Balanced approach with emphasis on stability '
                              'while allowing for moderate growth potential.')
            },
            'Moderate': {
                'score_range': (46, 65),
                'allocation': {
                    'Local equity': 20,
                    'Local bonds': 45,
                    'Local cash': 20,
                    'Global assets': 15
                },
                'description': ('Balanced strategy aiming for long-term capital growth '
                              'while maintaining reasonable stability.')
            },
            'Aggressive': {
                'score_range': (66, 77),
                'allocation': {
                    'Local equity': 25,
                    'Local bonds': 45,
                    'Local cash': 15,
                    'Global assets': 15
                },
                'description': ('Growth-oriented approach for investors comfortable '
                              'with higher volatility for potentially higher returns.')
            }
        }

    def setup_prompt_templates(self):
        """Setup prompt templates for risk profiling"""
        self.risk_assessment_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an investment risk profiling expert. Analyze the user's information 
            and determine their risk profile score (20-77) based on these factors:
            
            1. Age: Younger investors can typically take more risk (higher score)
            2. Job stability: Stable jobs allow for more risk tolerance
            3. Investment knowledge: More knowledge enables higher risk tolerance
            
            Score ranges:
            - Conservative: 20-30
            - Cautious: 31-45
            - Moderate: 46-65
            - Aggressive: 66-77
            
            Provide only the numerical score in your response."""),
            ("human", "{input}")
        ])

    def calculate_risk_score(self, user_data: Dict[str, Any]) -> int:
        """Calculate initial risk score based on user data"""
        # Age factor (20-35: +20, 36-50: +15, 51-65: +10, 65+: +5)
        try:
            age = int(user_data.get('age', 0))
            age_score = 20 if 20 <= age <= 35 else \
                       15 if 36 <= age <= 50 else \
                       10 if 51 <= age <= 65 else 5
        except:
            age_score = 10  # Default if age parsing fails

        # Job stability factor
        job = user_data.get('job', '').lower()
        stable_job_keywords = ['professional', 'engineer', 'doctor', 'teacher', 'permanent', 'full-time']
        job_score = 15 if any(keyword in job for keyword in stable_job_keywords) else \
                   10 if 'student' in job else \
                   5  # Default for other jobs

        # Base score (ensures minimum threshold)
        base_score = 20

        total_score = base_score + age_score + job_score
        
        # Ensure score stays within valid range
        return max(20, min(77, total_score))

    def determine_risk_profile(self, score: int) -> str:
        """Determine risk profile based on score"""
        for profile, details in self.risk_profiles.items():
            min_score, max_score = details['score_range']
            if min_score <= score <= max_score:
                return profile
        return 'Moderate'  # Default fallback

    def get_allocation(self, profile: str) -> Dict[str, int]:
        """Get asset allocation for given risk profile"""
        return self.risk_profiles[profile]['allocation']

    def get_profile_description(self, profile: str) -> str:
        """Get description for given risk profile"""
        return self.risk_profiles[profile]['description']

    async def create_profile(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create complete investment profile based on form data"""
        # Calculate risk score
        risk_score = self.calculate_risk_score(form_data)
        
        # Determine profile
        profile = self.determine_risk_profile(risk_score)
        
        # Get allocation and description
        allocation = self.get_allocation(profile)
        description = self.get_profile_description(profile)

        return {
            'profile': profile,
            'risk_score': risk_score,
            'allocation': allocation,
            'description': description,
            'user_info': {
                'name': form_data.get('fullName', ''),
                'age': form_data.get('age', ''),
                'job': form_data.get('job', '')
            }
        }

    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process incoming messages during allocation process"""
        try:
            # Basic response for continuing the conversation
            return {
                'type': 'text',
                'content': ('Please provide the requested information to create your '
                          'personalized investment profile.')
            }
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Error processing message: {str(e)}"
            }

    def validate_form_data(self, form_data: Dict[str, Any]) -> bool:
        """Validate form data"""
        required_fields = ['fullName', 'job', 'age', 'phoneNumber', 'email']
        
        # Check all required fields are present
        if not all(field in form_data for field in required_fields):
            return False
            
        # Check for empty values
        if any(not form_data[field] for field in required_fields):
            return False
            
        # Validate age is numeric and within reasonable range
        try:
            age = int(form_data['age'])
            if not (18 <= age <= 100):
                return False
        except ValueError:
            return False
            
        # Basic email format validation
        if '@' not in form_data['email']:
            return False
            
        return True

    async def explain_allocation(self, profile_data: Dict[str, Any]) -> str:
        """Generate explanation for the allocation"""
        profile = profile_data['profile']
        allocation = profile_data['allocation']
        
        explanation = (
            f"Based on your profile ({profile}), here's why this allocation is recommended:\n\n"
            f"• {allocation['Local equity']}% Local Equity: "
            f"This provides growth potential through South African companies.\n"
            f"• {allocation['Local bonds']}% Local Bonds: "
            f"Offers stability and regular income.\n"
            f"• {allocation['Local cash']}% Local Cash: "
            f"Provides liquidity and safety.\n"
            f"• {allocation['Global assets']}% Global Assets: "
            f"Adds international diversification.\n\n"
            f"{self.risk_profiles[profile]['description']}"
        )
        
        return explanation
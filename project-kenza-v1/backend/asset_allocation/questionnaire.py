from backend.asset_allocation.questions import QUESTIONS, RISK_PROFILES
from backend.config.config import Config

class RiskProfiler:
    def __init__(self):
        self.total_score = 0
        self.answers = {}
        self.current_question = None
        self.personal_info = {field: None for field in Config.PERSONAL_INFO_FIELDS}
        self.personal_info_complete = False
        self.assessment_complete = False

    def get_next_personal_info_field(self):
        """Get the next empty personal info field"""
        for field in Config.PERSONAL_INFO_FIELDS:
            if not self.personal_info[field]:
                return field
        self.personal_info_complete = True
        return None

    def set_personal_info(self, field: str, value: str):
        """Set personal information field"""
        if field in self.personal_info:
            self.personal_info[field] = value

    def process_answer(self, answer: str):
        """Process an answer to the current question"""
        if not self.current_question:
            self.current_question = 'Q1'
            return {
                "complete": False,
                "next_question": QUESTIONS['Q1']['text']
            }

        # Process current answer
        question = QUESTIONS[self.current_question]
        answer = answer.lower().strip()
        if answer in question['options']:
            score = question['options'][answer][1]
            self.answers[self.current_question] = answer
            self.total_score += score

            # Get next question
            current_num = int(self.current_question[1:])
            next_num = current_num + 1
            next_question = f'Q{next_num}'

            if next_question in QUESTIONS:
                self.current_question = next_question
                return {
                    "complete": False,
                    "next_question": QUESTIONS[next_question]['text']
                }
            else:
                self.assessment_complete = True
                return {
                    "complete": True,
                    "profile": self.get_profile()
                }

        return {
            "complete": False,
            "next_question": "Invalid answer. " + question['text']
        }

    def get_profile(self):
        """Get risk profile based on total score"""
        return Config.get_risk_profile(self.total_score)

    def get_current_state(self):
        """Get current state of profiling"""
        return {
            "personal_info": self.personal_info,
            "personal_info_complete": self.personal_info_complete,
            "current_question": self.current_question,
            "total_score": self.total_score,
            "assessment_complete": self.assessment_complete,
            "profile": self.get_profile() if self.assessment_complete else None
        }
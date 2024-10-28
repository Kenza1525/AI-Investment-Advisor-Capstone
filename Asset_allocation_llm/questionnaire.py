from questions import QUESTIONS, RISK_PROFILES

class RiskProfiler:
    def __init__(self):
        self.total_score = 0
        self.answers = {}
        self.current_section = None

    def ask_questions(self):
        print("\nInvestment Risk Profile Questionnaire\n")
        print("This questionnaire will help determine your investment risk profile and provide appropriate asset allocation recommendations.\n")
        print("Please answer each question by entering the letter (a, b, c, or d) corresponding to your choice.\n")
        
        for q_num, question in QUESTIONS.items():
            if question['section'] != self.current_section:
                self.current_section = question['section']
                print(f"\n{'-'*20}\nSection: {self.current_section}\n{'-'*20}\n")
            
            self._ask_single_question(q_num, question)

    def _ask_single_question(self, q_num, question):
        print(f"\n{q_num}. {question['text']}\n")
        for option, (text, _) in question['options'].items():
            print(f"{option}) {text}")
        
        while True:
            answer = input("\nYour answer (enter a, b, c, or d): ").lower().strip()
            answer = answer.split(')')[0].split('.')[0].strip()
            if answer in question['options']:
                score = question['options'][answer][1]
                self.answers[q_num] = answer
                self.total_score += score
                break
            print(f"Invalid option. Please enter one of: {', '.join(question['options'].keys())}")

    def get_profile(self):
        for (min_score, max_score), (profile, allocation) in RISK_PROFILES.items():
            if min_score <= self.total_score <= max_score:
                return profile, allocation
        return None, None
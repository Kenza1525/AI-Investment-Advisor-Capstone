import matplotlib.pyplot as plt

class AllocationVisualizer:
    @staticmethod
    def create_pie_chart(allocation, risk_profile):
        plt.figure(figsize=(10, 8))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        wedges, texts, autotexts = plt.pie(
            allocation.values(),
            labels=allocation.keys(),
            colors=colors,
            autopct='%1.1f%%',
            startangle=90
        )
        
        # Enhance text properties
        plt.setp(autotexts, size=9, weight="bold")
        plt.setp(texts, size=10)
        
        plt.title(f'Asset Allocation for {risk_profile} Risk Profile\n', 
                 fontsize=16, pad=20)
        
        # Add a legend
        plt.legend(
            wedges,
            allocation.keys(),
            title="Asset Classes",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        
        plt.axis('equal')
        plt.savefig('allocation_chart.png', bbox_inches='tight', dpi=300)
        plt.close()

# questionnaire.py
class RiskProfiler:
    def __init__(self):
        self.total_score = 0
        self.answers = {}
        self.current_section = None

    def ask_questions(self):
        print("\nInvestment Risk Profile Questionnaire\n")
        print("This questionnaire will help determine your investment risk profile and provide appropriate asset allocation recommendations.\n")
        
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
            answer = input("\nYour answer: ").lower()
            if answer in question['options']:
                score = question['options'][answer][1]
                self.answers[q_num] = answer
                self.total_score += score
                break
            print("Invalid option. Please try again.")

    def get_profile(self):
        for (min_score, max_score), (profile, allocation) in RISK_PROFILES.items():
            if min_score <= self.total_score <= max_score:
                return profile, allocation
        return None, None
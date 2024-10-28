from questions import QUESTIONS
class RiskBasedAllocator:
    def __init__(self, risk_assessment_responses: dict):
        self.score = 0
        self.asset_classes = {
                "Local equity": {},
                "Local bonds": {},
                "Local cash": {},
                "Global assets": {}
}
        self.answer1 = risk_assessment_responses["question1"].lower()
        self.answer2 = risk_assessment_responses["question2"].lower()
        self.answer3 = risk_assessment_responses["question3"].lower()
        self.answer4 = risk_assessment_responses["question4"].lower()
        self.answer5 = risk_assessment_responses["question5"].lower()
        self.answer6 = risk_assessment_responses["question6"].lower()
        self.answer7 = risk_assessment_responses["question7"].lower()
        self.answer8 = risk_assessment_responses["question8"].lower()
        self.answer9 = risk_assessment_responses["question9"].lower()
        self.answer10 = risk_assessment_responses["question10"].lower()
        self.answer11 = risk_assessment_responses["question11"].lower() 

    def calculate_risk_tolerance(self):
        # Calculate the risk score based on the user's responses
        self.score = (
                    QUESTIONS["Q1"]["options"][self.answer1][1] +
                    QUESTIONS["Q2"]["options"][self.answer2][1] +
                    QUESTIONS["Q3"]["options"][self.answer3][1] +
                    QUESTIONS["Q4"]["options"][self.answer4][1] +
                    QUESTIONS["Q5"]["options"][self.answer5][1] +
                    QUESTIONS["Q6"]["options"][self.answer6][1] +
                    QUESTIONS["Q7"]["options"][self.answer7][1] +
                    QUESTIONS["Q8"]["options"][self.answer8][1] +
                    QUESTIONS["Q9"]["options"][self.answer9][1] +
                    QUESTIONS["Q10"]["options"][self.answer10][1]+
                    QUESTIONS["Q11"]["options"][self.answer11][1]
)
        if self.score <= 30:
            return "Conservative"
        elif 31 <= self.score <= 45:
            return "Cautious"
        elif 46 <= self.score < 65:
            return "Moderate"
        elif self.score > 65:
            return "Aggressive"
        else:
            return "Unknown"
        
    def risk_base_allocation(self):
        risk_tolerance = self.calculate_risk_tolerance()
        if risk_tolerance == "Conservative":
            self.asset_classes["Local equity"] = 0.10
            self.asset_classes["Local bonds"] = 0.50
            self.asset_classes["Local cash"] = 0.25
            self.asset_classes["Global assets"] = 0.15

        elif risk_tolerance == "Cautious":
            self.asset_classes["Local equity"] = 0.15
            self.asset_classes["Local bonds"] = 0.50
            self.asset_classes["Local cash"] = 0.20
            self.asset_classes["Global assets"] = 0.15

        elif risk_tolerance == "Moderate":
            self.asset_classes["Local equity"] = 0.20
            self.asset_classes["Local bonds"] = 0.45
            self.asset_classes["Local cash"] = 0.20
            self.asset_classes["Global assets"] = 0.15

        elif risk_tolerance == "Aggressive":
            self.asset_classes["Local equity"] = 0.25
            self.asset_classes["Local bonds"] = 0.45
            self.asset_classes["Local cash"] = 0.15
            self.asset_classes["Global assets"] = 0.15
        return self.asset_classes

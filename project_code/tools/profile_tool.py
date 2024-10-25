class UserProfile:
    def __init__(self, name, age, financial_goal, investment_horizon, risk_tolerance):
        self.name = name
        self.age = age
        self.financial_goal = financial_goal
        self.investment_horizon = investment_horizon
        self.risk_tolerance = risk_tolerance
        self.investment_options = {
            "bonds": {"Risk": 1, "Return": 3},
            "Stocks": {"Risk": 2, "Return": 10},
            "Commodities": {"Risk": 2, "Return": 10},
            "Cryptocurrencies": {"Risk": 3, "Return": 15}
        }
    
    def get_risk_profile(self):
        # Define the risk categories based on risk tolerance
        risk_categories = {
            "Conservative": ["bonds"],
            "Moderate": ["Commodities", "Stocks"],
            "Aggressive": ["Stocks", "Cryptocurrencies", "Commodities"]
        }

        # Return the risk profile categories based on the user's risk tolerance
        if self.risk_tolerance == "Conservative":
            return risk_categories["Conservative"]
        elif self.risk_tolerance == "Moderate":
            return risk_categories["Moderate"]
        elif self.risk_tolerance == "Aggressive":
            return risk_categories["Aggressive"]

    def categorize_investments(self):
        # Get the recommended asset categories based on the risk profile
        recommended_assets = self.get_risk_profile()

        # Filter and categorize the investment options based on the recommended assets
        categorized_investments = {}
        for asset in recommended_assets:
            if asset in self.investment_options:
                categorized_investments[asset] = self.investment_options[asset]
        
        return categorized_investments
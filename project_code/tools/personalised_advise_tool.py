from tools.market_analysis import MarketAnalysisTool
from tools.profile_tool import UserProfile

class PersonalizedAdviceTool:
    def __init__(self, api_key):
        self.api_key = api_key
        self.market_tool = MarketAnalysisTool(api_key=api_key)

    def provide_advice(self, user_profile: UserProfile, sum_of_money):
        # Get the user's risk profile from the UserProfile class
        recommended_assets = user_profile.get_risk_profile()

        # Categorize the recommended assets using the UserProfile method
        categorized_investments = user_profile.categorize_investments()

        # Fetch market analysis using MarketAnalysisTool
        rankings = self.market_tool.analyze_and_rank()

        # Handle case where market data is unavailable
        if not rankings:
            return {"bonds": sum_of_money}

        # Filter the rankings to only include categories from the user's risk profile
        filtered_rankings = [(category, score) for category, score in rankings if category in categorized_investments]

        # If no valid filtered rankings are available, apply a conservative fallback
        if not filtered_rankings:
            return {"bonds": sum_of_money}
           

        # Adjust rankings based on the user's risk tolerance
        adjusted_rankings = self.adjust_allocation_based_on_profile(filtered_rankings, user_profile.risk_tolerance)

        # If no valid rankings were returned, apply a conservative fallback
        if not adjusted_rankings:
            return {"bonds": sum_of_money}

        # Distribute the investment amount based on adjusted rankings
        total_score = sum(score for _, score in adjusted_rankings)
        investment_distribution = {
            category: round((score / total_score) * sum_of_money, 2)
            for category, score in adjusted_rankings
        }

        return  investment_distribution

    def adjust_allocation_based_on_profile(self, rankings, risk_tolerance):
        # Adjust allocation based on user's risk profile
        adjustment_factor = 1.2 if risk_tolerance == "Aggressive" else 0.8
        adjusted_rankings = []

        for category, score in rankings:
            # Increase allocation for high-risk assets if the user is Aggressive
            if category in ["Cryptocurrencies", "Stocks"] and risk_tolerance == "Aggressive":
                score *= adjustment_factor
            # Decrease allocation for low-risk assets if the user is Conservative
            elif category in ["bonds"] and risk_tolerance == "Conservative":
                score *= (1 / adjustment_factor)
            adjusted_rankings.append((category, score))

        return adjusted_rankings
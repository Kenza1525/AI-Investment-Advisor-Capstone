# tools/general_advice_tool.py

from tools.market_analysis import MarketAnalysisTool

class GeneralAdviceTool:

    def __init__(self, api_key):
        self.api_key = api_key
        self.market_tool = MarketAnalysisTool(api_key=api_key)

    def provide_advice(self, sum_of_money=None):
        # Fetch market analysis using MarketAnalysisTool
        rankings = self.market_tool.analyze_and_rank()

        if not rankings:
            return "Unable to fetch market data."

        if sum_of_money:
            total_score = sum(score for category, score in rankings)
            investment_distribution = {
                category: round((score / total_score) * sum_of_money, 2)
                for category, score in rankings
            }
            return investment_distribution
        return rankings  # Return the rankings if no money is specified


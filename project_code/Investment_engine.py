#User Profiling

class UserProfile:
    def __init__(self, name, age, income, financial_goal, investment_horizon, risk_tolerance):
        self.name = name
        self.age = age
        self.income = income
        self.financial_goal = financial_goal
        self.investment_horizon = investment_horizon
        self.risk_tolerance = risk_tolerance
        #self.monthly_addition = additon



    def display_profile(self):
        print(f"User: {self.name}, Age: {self.age}")
        print(f"Income: {self.income}")
        print(f"Financial Goal: {self.financial_goal}")
        print(f"Investment Horizon: {self.investment_horizon}")
        print(f"Risk Tolerance: {self.risk_tolerance}")

# Example user input
# user = UserProfile(
#     name="John Doe", 
#     age=35, 
#     income=60000, 
#     financial_goal="Retirement", 
#     investment_horizon=25, 
#     risk_tolerance="Moderate"
# )

# user.display_profile()

#Risk profiling
def risk_profile(user):
    risk_categories = {
        "Conservative": ["Low-risk bonds", "Fixed deposits"],
        "Moderate": ["Balanced mutual funds", "Index funds", "Corporate bonds"],
        "Aggressive": ["Stocks", "Cryptocurrencies", "Emerging markets"]
    }

    if user.risk_tolerance == "Conservative":
        return risk_categories["Conservative"]
    elif user.risk_tolerance == "Moderate":
        return risk_categories["Moderate"]
    elif user.risk_tolerance == "Aggressive":
        return risk_categories["Aggressive"]

# Example
# recommended_risks = risk_profile(user)
# print(f"Recommended Asset Classes for {user.name}: {recommended_risks}")

#Investment options
investment_options = {
    "Low-risk bonds": {"Risk": 1, "Return": 3},
    "Fixed deposits": {"Risk": 1, "Return": 2},
    "Balanced mutual funds": {"Risk": 3, "Return": 6},
    "Index funds": {"Risk": 4, "Return": 7},
    "Corporate bonds": {"Risk": 3, "Return": 5},
    "Stocks": {"Risk": 6, "Return": 10},
    "Cryptocurrencies": {"Risk": 9, "Return": 15},
    "Emerging markets": {"Risk": 8, "Return": 12}
}

def categorize_investments(recommended_assets):
    categorized_investments = {}
    for asset in recommended_assets:
        if asset in investment_options:
            categorized_investments[asset] = investment_options[asset]
    return categorized_investments

# Example
# categorized_investments = categorize_investments(recommended_risks)
# print("Categorized Investments:")
# for asset, details in categorized_investments.items():
#     print(f"{asset}: Risk = {details['Risk']}, Return = {details['Return']}")


#Portfolio construction

import numpy as np
def random_weights(n):
    weights = np.random.rand(n)
    return weights / sum(weights)

def portfolio_return(weights, returns):
    return np.dot(weights, returns)

def portfolio_risk(weights, risks):
    return np.sqrt(np.dot(weights.T, np.dot(np.cov(risks), weights)))

# Example - Random portfolio construction
# assets = list(categorized_investments.keys())
# returns = [investment_options[asset]["Return"] for asset in assets]
# risks = [investment_options[asset]["Risk"] for asset in assets]

# weights = random_weights(len(assets))
# expected_return = portfolio_return(weights, returns)
# expected_risk = portfolio_risk(weights, risks)

# print(f"Portfolio Weights: {weights}")
# print(f"Expected Portfolio Return: {expected_return:.2f}%")
# print(f"Expected Portfolio Risk: {expected_risk:.2f}")


#Porfolio rebalancing
def rebalance_portfolio(weights, target_allocation):
    new_weights = np.array(target_allocation)
    return new_weights / sum(new_weights)

# Example
# target_allocation = [0.3, 0.4, 0.2, 0.1]  # New target allocation for the 4 assets
# new_weights = rebalance_portfolio(weights, target_allocation)
# print(f"New Portfolio Weights after Rebalancing: {new_weights}")


#Monitoring the portfolio

def monitor_portfolio(weights, returns, risks):
    current_return = portfolio_return(weights, returns)
    current_risk = portfolio_risk(weights, risks)
    
    print(f"Monitoring Portfolio: Return = {current_return:.2f}%, Risk = {current_risk:.2f}")

# Example monitoring
# monitor_portfolio(new_weights, returns, risks)


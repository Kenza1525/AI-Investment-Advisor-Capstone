'''These functions are used to fetch Yahoo finance market summary data. The data is then categorized into different asset classes 
such as stocks, commodities, bonds, cryptocurrencies, forex, and others. The average performance of each asset class is calculated 
based on the price change and percent change. The data is then normalized and ranked based on the combined score of price change and percent change. 
The ranked asset classes are then displayed used to recommend investment options to users that are not asking for personalized advise. 
This ensures that the advise/recommendations are based on current market performance data which is very relevant.'''

import requests
class MarketAnalysisTool:
    def __init__(self, api_key="KYpAilMplU1cVSK0H7N1P5OoR2znLbsIJa9yOER1"):
        self.api_key = api_key

    def get_market_summary(self):
        """
        Fetch the market summary data from Yahoo Finance API.
        """
        url = "https://yfapi.net/v6/finance/quote/marketSummary"
        headers = {
            'x-api-key': self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            market_data = response.json()
            return market_data
        else:
            print(f"Error: Unable to fetch data, status code {response.status_code}")
            return None

    def categorize_market_data(self, market_data):
        """
        Categorize the market data into Stocks, Commodities, Bonds, Cryptocurrencies, Forex, and Others.
        """
        categorized_data = {
            "Stocks": [],
            "Commodities": [],
            "Bonds": [],
            "Cryptocurrencies": [],
            "Forex": [],
            "Others": []
        }

        for market in market_data['marketSummaryResponse']['result']:
            quote_type = market.get('quoteType', '').lower()
            full_exchange_name = market.get('fullExchangeName', '').lower()

            if quote_type == "index" and ("snp" in full_exchange_name or "nasdaq" in full_exchange_name or "ftse" in full_exchange_name):
                category = "Stocks"
            elif quote_type == "future" or "mercantile" in full_exchange_name or "comex" in full_exchange_name:
                category = "Commodities"
            elif quote_type == "index" and "bond" in full_exchange_name:
                category = "Bonds"
            elif quote_type == "cryptocurrency":
                category = "Cryptocurrencies"
            elif quote_type == "currency":
                category = "Forex"
            else:
                category = "Others"

            categorized_data[category].append({
                "Price Change": float(market['regularMarketChange']['raw']),
                "Percent Change": float(market['regularMarketChangePercent']['raw'])
            })
        return categorized_data

    def calculate_average_performance(self, categorized_data):
        """
        Calculate the average performance (price change and percentage change) for each asset class.
        """
        average_performance = {}
        for category, data in categorized_data.items():
            if data:
                total_price_change = sum(item['Price Change'] for item in data)
                total_percent_change = sum(item['Percent Change'] for item in data)
                count = len(data)
                average_performance[category] = {
                    "Average Price Change": total_price_change / count,
                    "Average Percent Change": total_percent_change / count
                }
        return average_performance

    def normalize_data(self, data):
        """
        Normalize the data to bring the values into the range [0, 1].
        """
        max_value = max(data)
        min_value = min(data)
        return [(x - min_value) / (max_value - min_value) for x in data]

    def rank_with_normalization(self, average_performance):
        """
        Rank the asset classes based on normalized scores of price change and percent change.
        """
        rankings = []
        price_changes = [performance['Average Price Change'] for performance in average_performance.values()]
        percent_changes = [performance['Average Percent Change'] for performance in average_performance.values()]
        normalized_prices = self.normalize_data(price_changes)
        normalized_percents = self.normalize_data(percent_changes)

        categories = list(average_performance.keys())
        for i, category in enumerate(categories):
            combined_score = 0.5 * normalized_prices[i] + 0.5 * normalized_percents[i]
            rankings.append((category, combined_score))

        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings

    def analyze_and_rank(self):
        """
        Fetch, categorize, calculate, and rank the asset classes.
        """
        market_summary = self.get_market_summary()
        if market_summary:
            categorized_data = self.categorize_market_data(market_summary)
            average_performance = self.calculate_average_performance(categorized_data)
            rankings = self.rank_with_normalization(average_performance)
            return rankings
        else:
            return None


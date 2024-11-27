class PortfolioForecaster:
    def __init__(self, initial_allocations, horizon, inflation_rate=0.02):
        self.initial_allocations = initial_allocations
        self.time_horizon = horizon
        self.inflation_rate = inflation_rate
        
        # Example annual growth rates for each asset class 
        self.growth_rates = {
            "Local equity": 0.10,
            "Local bonds": 0.05,
            "Local cash": 0.00,
            "Global assets": 0.07
        }
    
    def forecast_growth(self):
        forecast = {str(year): {} for year in range(self.time_horizon + 1)}  
        
        for asset_class, initial_amount in self.initial_allocations.items():
            growth_rate = self.growth_rates.get(asset_class, 0.0)
            current_value = initial_amount
            for year in range(self.time_horizon + 1):
                current_value = current_value * (1 + growth_rate) / (1 + self.inflation_rate)
                
                forecast[str(year)][asset_class] = current_value 
        
        formatted_forecast = {
            "years": list(map(str, range(self.time_horizon + 1))),
            "asset_values": {
                asset_class: [forecast[str(year)][asset_class] for year in range(self.time_horizon + 1)]
                for asset_class in self.initial_allocations.keys()
            },
            "metadata": {
                "horizon": self.time_horizon,
                "inflation_rate": self.inflation_rate
            }
        }
        
        return formatted_forecast
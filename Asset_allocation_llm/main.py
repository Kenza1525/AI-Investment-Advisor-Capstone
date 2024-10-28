from questionnaire import RiskProfiler
from visualizer import AllocationVisualizer
from llm_tool import AssetAllocationAdvisor

def main():
    print("Welcome to the Investment Risk Profiling System")
    print("="*50)
    
    advisor = AssetAllocationAdvisor()
    
    while True:
        print("\nPlease choose an option:")
        print("1. Take the risk profile questionnaire")
        print("2. Ask questions about asset allocation and risk profiling")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            profiler = RiskProfiler()
            profiler.ask_questions()
            
            profile, allocation = profiler.get_profile()
            
            print("\n" + "="*50)
            print("Risk Profile Analysis Results")
            print("="*50)
            print(f"\nTotal Score: {profiler.total_score}")
            print(f"Risk Profile: {profile}")
            
            if profile and allocation:
                print("\nRecommended Asset Allocation:")
                for asset, percentage in allocation.items():
                    print(f"{asset}: {percentage}%")
                
                AllocationVisualizer.create_pie_chart(allocation, profile)
                print("\nA detailed asset allocation chart has been generated as 'allocation_chart.png'")
            else:
                print("\nError: Could not determine risk profile. Please consult a financial advisor.")
                
        elif choice == "2":
            print("\nYou can ask questions about:")
            print("- How risk profiles are determined")
            print("- Asset allocation strategies")
            print("- Investment objectives and time horizons")
            print("- Risk tolerance assessment")
            print("(Type 'exit' to return to main menu)")
            
            while True:
                question = input("\nWhat would you like to know? ")
                if question.lower() == 'exit':
                    break
                    
                response = advisor.get_response(question)
                print("\nResponse:", response)
                print("\n" + "="*50)
                
        elif choice == "3":
            print("\nThank you for using the Investment Risk Profiling System!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
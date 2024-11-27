import json
import chainlit as cl
import asyncio
from backend.profiles_db import UserProfileDatabase
from backend.education.chat_hypo import (
    setup_agent, 
    user_info, 
    investment_details,
    PortfolioForecaster
)




from backend.asset_allocation.questions import QUESTIONS, RISK_PROFILES

db = UserProfileDatabase()


class FinancialAdvisor:
    def __init__(self):
        self.agent = None
        self.reset_state()
        self.full_name = ""

    def reset_state(self):
        """Reset state variables"""
        self.collecting_personal_info = False
        self.current_question = None
        self.risk_assessment = {
            "total_score": 0,
            "answered_questions": []
        }
        self.personal_info_fields = [
            ('fullName', 'What is your full name?'),
            ('job', 'What is your occupation?'),
            ('age', 'What is your age?'),
            ('phoneNumber', 'What is your phone number?'),
            ('email', 'What is your email address?'),
            ('investment_amount', 'How much would you like to invest? (Enter amount in numbers)'),
            ('time_horizon', 'What is your investment time horizon in years? (Enter number of years)')
        ]
        self.current_field_index = 0

    async def initialize(self):
        """Initialize the advisor"""
        try:
            self.agent = await setup_agent()
            self.reset_state()
            cl.user_session.set("advisor", self)
        except Exception as e:
            print(f"Error initializing advisor: {str(e)}")
            raise

    async def handle_personal_info(self, message: str):
        """Handle personal information collection"""
        global profiles
        try:
            if self.current_field_index >= len(self.personal_info_fields):
                self.collecting_personal_info = False
                
                # Store investment details
                if 'investment_amount' in user_info:
                    investment_details['amount'] = float(user_info['investment_amount'])
                if 'time_horizon' in user_info:
                    investment_details['time_horizon'] = int(user_info['time_horizon'])
                
                # Update frontend with complete personal info
                await cl.CopilotFunction(
                    name="update_personal_info",
                    args=user_info
                ).acall()

                self.full_name = user_info["fullName"]
                # print("Full name", full_name)
                print("Personal info collected:", user_info)
                # with open("data.json", "w") as f:
                #     json.dump(user_info, f)
                db.create_profile(user_info)
                profiles = db.read_profiles()
                print(profiles)


                
                # Start risk assessment
                self.current_question = 'Q1'
                await self.show_risk_question('Q1')
                return

            field, question = self.personal_info_fields[self.current_field_index]
            
            # Validate and store the current answer
            try:
                if field in ['investment_amount', 'time_horizon']:
                    value = float(message) if field == 'investment_amount' else int(message)
                    if value <= 0:
                        raise ValueError("Value must be positive")
                    user_info[field] = value
                else:
                    if not message.strip():
                        raise ValueError("Field cannot be empty")
                    user_info[field] = message.strip()

                # Move to next field
                self.current_field_index += 1
                
                # Send personal info to frontend
                await cl.CopilotFunction(
                    name="update_personal_info",
                    args=user_info
                ).acall()

                # Ask next question if there are more
                if self.current_field_index < len(self.personal_info_fields):
                    next_field, next_question = self.personal_info_fields[self.current_field_index]
                    await cl.Message(content=next_question).send()
                else:
                    await self.handle_personal_info("")  # Trigger completion

            except ValueError as ve:
                await cl.Message(content=f"Invalid input: {str(ve)}. Please try again.").send()
                return

        except Exception as e:
            print(f"Error collecting personal info: {str(e)}")
            await cl.Message(content="I encountered an error. Let's try again.").send()
            self.reset_state()

    async def show_risk_question(self, question_id):
        """Display a risk assessment question"""
        try:
            question_text = QUESTIONS[question_id]['text']
            options = QUESTIONS[question_id]['options']
            formatted_options = "\n".join([
                f"{k}) {v[0]}" for k, v in options.items()
            ])
            
            await cl.Message(
                content=f"{question_text}\n\n{formatted_options}\n\n"
                        "Please answer with a single letter (a, b, c, or d)."
            ).send()
        except Exception as e:
            print(f"Error showing question: {str(e)}")
            await cl.Message(content="Error displaying question. Let's start over.").send()
            self.reset_state()

    async def process_risk_answer(self, answer: str):
        """Process risk assessment answer"""
        if not self.current_question or self.current_question not in QUESTIONS:
            return False

        answer = answer.strip().lower()
        if len(answer) == 1 and answer in QUESTIONS[self.current_question]['options']:
            score = QUESTIONS[self.current_question]['options'][answer][1]
            self.risk_assessment["total_score"] += score
            self.risk_assessment["answered_questions"].append(self.current_question)

            # Move to next question or finish assessment
            question_num = int(self.current_question[1:])
            next_q = f'Q{question_num + 1}'

            if next_q in QUESTIONS:
                self.current_question = next_q
                await self.show_risk_question(next_q)
            else:
                await self.calculate_profile()
            return True
        return False
    async def calculate_profile(self):
        """Calculate and show risk profile results"""

        global profiles
        
        score = self.risk_assessment["total_score"]
        
        for (min_score, max_score), (profile, allocation) in RISK_PROFILES.items():
            if min_score <= score <= max_score:
                investment_details['allocation'] = allocation
                
                try:
                    # Prepare allocation chart data
                    allocation_data = {
                        "profile": profile,
                        "allocation": allocation,
                        "score": score
                    }

                    # Generate forecast data if we have the necessary information
                    forecast_data = None
                    if investment_details.get('amount') and investment_details.get('time_horizon'):
                        # Calculate initial allocations
                        initial_allocations = {
                            asset: (percentage / 100) * investment_details['amount']
                            for asset, percentage in allocation.items()
                        }
                        
                        # Generate forecast using PortfolioForecaster
                        forecaster = PortfolioForecaster(
                            initial_allocations,
                            investment_details['time_horizon']
                        )
                        forecast_result = forecaster.forecast_growth()
                        
                        # Structure forecast data as expected by frontend
                        forecast_data = {
                            "lineChart": {
                                "years": forecast_result["years"],
                                "asset_values": forecast_result["asset_values"]
                            },
                            "finalPieChart": {
                                asset: values[-1] 
                                for asset, values in forecast_result["asset_values"].items()
                            }
                        }

                    # Send both visualizations simultaneously
                    update_tasks = [
                        cl.CopilotFunction(
                            name="update_allocation_chart", 
                            args=allocation_data
                        ).acall()
                    ]
                    print(self.full_name)
                    # db.update_portfolio(self.full_name, **allocation_data)
                    # print(profiles)
                    # print("updated portfolio")
                    # print("Allocation data", allocation_data)
                    
                    if forecast_data:
                        update_tasks.append(
                            cl.CopilotFunction(
                                name="update_forecast_charts",
                                args=forecast_data
                            ).acall()
                        )

                    # Execute all updates concurrently
                    await asyncio.gather(*update_tasks)
                    
                    # Prepare response message
                    message_content = [
                        f"Based on your answers:\n",
                        f"• Risk Profile: {profile}",
                        f"• Total Score: {score}\n"
                    ]
                    
                    if forecast_data:
                        message_content.append(
                            f"I've updated your portfolio visualization and generated a forecast "
                            f"for your {investment_details['amount']:,.2f} investment "
                            f"over {investment_details['time_horizon']} years.\n"
                        )
                    else:
                        message_content.append(
                            "I've updated your portfolio visualization.\n"
                        )
                    
                    message_content.append(
                        "You can ask me about your risk profile, allocation strategy, "
                        "or any other investment questions."
                    )
                    
                    await cl.Message(content="\n".join(message_content)).send()
                    return

                except Exception as e:
                    print(f"Error in profile calculation: {str(e)}")
                    await cl.Message(
                        content="I encountered an error while generating your investment profile. "
                                "Please try again."
                    ).send()
                    self.reset_state()
                    return

        await cl.Message(
            content=f"I couldn't determine a suitable risk profile for your score ({score}). "
            "Let's try the assessment again."
        ).send()
        self.reset_state()

    async def generate_forecast(self):
        """Generate and display portfolio forecast"""
        try:
            if not investment_details.get('amount') or not investment_details.get('time_horizon'):
                await cl.Message(
                    content="Missing investment amount or time horizon. Please provide complete information."
                ).send()
                return
                
            if not investment_details.get('allocation'):
                await cl.Message(
                    content="Portfolio allocation not yet determined. Please complete the risk assessment first."
                ).send()
                return

            # Calculate initial allocations
            initial_allocations = {
                asset: (percentage / 100) * investment_details['amount']
                for asset, percentage in investment_details['allocation'].items()
            }
            
            # Generate forecast
            forecaster = PortfolioForecaster(
                initial_allocations,
                investment_details['time_horizon']
            )
            forecast_result = forecaster.forecast_growth()
            
            # Structure data for frontend
            forecast_data = {
                "lineChart": {
                    "years": forecast_result["years"],
                    "asset_values": forecast_result["asset_values"]
                },
                "finalPieChart": {
                    asset: values[-1] 
                    for asset, values in forecast_result["asset_values"].items()
                }
            }
            
            # Send to frontend
            await cl.CopilotFunction(
                name="update_forecast_charts",
                args=forecast_data
            ).acall()
            
            await cl.Message(
                content=f"I've updated the forecast for your {investment_details['amount']:,.2f} "
                       f"investment over {investment_details['time_horizon']} years."
            ).send()
            
        except Exception as e:
            print(f"Error generating forecast: {str(e)}")
            await cl.Message(
                content="I encountered an error while generating the forecast. Please try again."
            ).send()

advisor = FinancialAdvisor()

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    await advisor.initialize()
    await cl.Message(
        content="Hello! I'm your investment advisor. I can help you with:\n"
                "• Investment education and market information\n"
                "• Personal investment profile creation\n"
                "• Portfolio allocation and forecasting\n\n"
                "To get started with personalized recommendations, I'll need some information from you. "
                "Would you like to proceed with creating your investment profile now?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    msg = message.content.strip()

    try:
        # If collecting personal info, handle that first
        if advisor.collecting_personal_info:
            await advisor.handle_personal_info(msg)
            return

        # If in risk assessment, process answers
        if advisor.current_question:
            if await advisor.process_risk_answer(msg):
                return

        # Check if user wants to start profile creation
        if any(keyword in msg.lower() for keyword in ['yes', 'proceed', 'profile', 'start']):
            if not advisor.collecting_personal_info and not advisor.current_question:
                advisor.collecting_personal_info = True
                field, question = advisor.personal_info_fields[0]
                await cl.Message(
                    content="Great! Let's start by getting some information from you.\n\n" + question
                ).send()
                return

        # For all other queries, use the agent
        if advisor.agent:
            response = await advisor.agent.run(msg)
            if response:
                await cl.Message(content=response).send()
        else:
            await cl.Message(
                content="The system is not properly initialized. Please refresh the page and try again."
            ).send()

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        await cl.Message(
            content="I apologize, but I encountered an error. Please try again."
        ).send()

@cl.on_chat_end
async def end():
    """Clean up on chat end"""
    advisor.reset_state()

if __name__ == "__main__":
    cl.run()
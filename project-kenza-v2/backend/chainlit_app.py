import chainlit as cl
from education.chat_hypo import setup_education_agent
from asset_allocation.questions import QUESTIONS, RISK_PROFILES

class AdvisorApp:
    def __init__(self):
        self.education_agent = None
        self.reset_state()

    def reset_state(self):
        """Reset all state variables"""
        self.current_mode = "choose_mode"
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
            ('email', 'What is your email address?')
        ]
        self.current_field_index = 0
        self.personal_info = {}
        self.collecting_personal_info = False

    async def initialize(self):
        """Initialize the advisor"""
        try:
            self.education_agent = await setup_education_agent()
            self.reset_state()
        except Exception as e:
            print(f"Error initializing advisor: {str(e)}")
            raise

    async def handle_education_mode(self, msg: str):
        """Handle education mode interactions"""
        try:
            if not self.education_agent:
                self.education_agent = await setup_education_agent()

            # Get response from education agent
            result = await self.education_agent.run(msg)
            
            # Send the educational response
            await cl.Message(content=result).send()
            
            # Ask if they want to continue with education or switch
            await cl.Message(
                content="\nWould you like to:\n1. Continue learning about investments\n"
                        "2. Switch to creating an investment profile\n\n"
                        "Please select 1 or 2 to proceed."
            ).send()

        except Exception as e:
            print(f"Error in education mode: {str(e)}")
            await cl.Message(
                content="I encountered an error processing your question. Let's try again.\n\n"
                        "What would you like to know about investing?"
            ).send()

    async def collect_personal_info(self, message: str):
        """Handle personal information collection"""
        try:
            if self.current_field_index >= len(self.personal_info_fields):
                self.collecting_personal_info = False
                self.current_mode = "risk_assessment"
                self.current_question = 'Q1'

                # Send the first risk assessment question
                await cl.Message(
                    content=f"Thank you for providing your information, {self.personal_info.get('fullName', '')}.\n\n"
                            "Now, I'll help determine your ideal asset allocation through a series of questions.\n\n"
                            f"{QUESTIONS['Q1']['text']}\n\n" +
                            "\n".join([f"{k}) {v[0]}" for k, v in QUESTIONS['Q1']['options'].items()]) +
                            "\n\nPlease answer with a single letter (a, b, c, or d)."
                ).send()
                return

            # Collect current personal info
            field, question = self.personal_info_fields[self.current_field_index]
            self.personal_info[field] = message

            # Move to next field
            self.current_field_index += 1

            # Ask next question or proceed to risk assessment
            if self.current_field_index < len(self.personal_info_fields):
                next_field, next_question = self.personal_info_fields[self.current_field_index]
                await cl.Message(content=next_question).send()
            else:
                await self.collect_personal_info("")

        except Exception as e:
            print(f"Error collecting personal info: {str(e)}")
            await cl.Message(content="I encountered an error. Let's try again.").send()
            self.reset_state()

    def process_answer(self, answer: str):
        """Process answer for risk assessment questions"""
        if not self.current_question or self.current_question not in QUESTIONS:
            return False, 0

        answer = answer.strip().lower()
        if len(answer) == 1 and answer in QUESTIONS[self.current_question]['options']:
            score = QUESTIONS[self.current_question]['options'][answer][1]
            return True, score
        return False, 0

    async def calculate_and_show_profile(self):
        """Calculate risk profile and show results"""
        try:
            score = self.risk_assessment["total_score"]
            
            for (min_score, max_score), (profile, allocation) in RISK_PROFILES.items():
                if min_score <= score <= max_score:
                    # Send profile information directly to Chainlit
                    response = (
                        f"Based on your answers, here is your investment profile:\n\n"
                        f"• Risk Profile: {profile}\n"
                        f"• Total Score: {score}\n\n"
                        "Here's your recommended asset allocation:\n\n"
                    )

                    for asset, percentage in allocation.items():
                        response += f"• {asset}: {percentage}%\n"

                    # Prepare chart data for JavaScript
                    chart_data = {
                        "allocation": allocation
                    }

                    # Send chart data to frontend
                    await cl.Message(content=response).send()
                    
                    # Use Chainlit's built-in functions to send data to frontend
                    await cl.make_async_call("update_chart", chart_data)
                    
                    # Ask for next action
                    await cl.Message(
                        content="\nWould you like to:\n"
                                "1. Continue learning about investments and the JSE\n"
                                "2. Create another investment profile\n\n"
                                "Please select 1 or 2 to proceed."
                    ).send()
                    
                    self.current_mode = "choose_mode"
                    return

            # No profile match found
            self.reset_state()
            await cl.Message(content=f"I couldn't determine a suitable risk profile for your score ({score}). Let's try again.").send()

        except Exception as e:
            print(f"Error in profile calculation: {str(e)}")
            self.reset_state()
            await cl.Message(content="I encountered an error calculating your risk profile. Let's try again.").send()

advisor = AdvisorApp()

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    await advisor.initialize()
    await cl.Message(
        content="Hello! I'm your investment advisor. I can help you with:\n\n"
                "1. Learning about investments and the JSE\n"
                "2. Creating a personalized investment profile and asset allocation\n\n"
                "Please select 1 or 2 to proceed."
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    msg = message.content.strip()

    try:
        # Handle personal information collection mode
        if advisor.collecting_personal_info:
            await advisor.collect_personal_info(msg)
            return

        # Handle mode selection
        if msg == "2" or (advisor.current_mode == "choose_mode" and msg == "2"):
            advisor.collecting_personal_info = True
            advisor.current_mode = "personal_info"
            field, question = advisor.personal_info_fields[0]
            await cl.Message(
                content="Before we begin the risk assessment, I'll need some information from you.\n\n" + question
            ).send()
            return

        elif msg == "1" or (advisor.current_mode == "choose_mode" and msg == "1"):
            advisor.current_mode = "education"
            await cl.Message(
                content="What would you like to know about investing? I can help you understand stocks, bonds, mutual funds, or any other investment topics.\n\n"
                        "(After each answer, I'll ask if you want to continue with education (1) or switch to asset allocation (2))"
            ).send()
            return

        # Handle risk assessment mode
        if advisor.current_mode == "risk_assessment":
            is_valid, score = advisor.process_answer(msg)

            if not is_valid:
                await cl.Message(
                    content="Please select one of the provided options (a, b, c, or d):\n\n" +
                            f"{QUESTIONS[advisor.current_question]['text']}\n\n" +
                            "\n".join([f"{k}) {v[0]}" for k, v in QUESTIONS[advisor.current_question]['options'].items()])
                ).send()
                return

            advisor.risk_assessment["total_score"] += score
            advisor.risk_assessment["answered_questions"].append(advisor.current_question)

            question_num = int(advisor.current_question[1:])
            next_q = f'Q{question_num + 1}'

            if next_q in QUESTIONS:
                advisor.current_question = next_q
                await cl.Message(
                    content=f"{QUESTIONS[next_q]['text']}\n\n" +
                            "\n".join([f"{k}) {v[0]}" for k, v in QUESTIONS[next_q]['options'].items()]) +
                            "\n\nPlease answer with a single letter (a, b, c, or d)."
                ).send()
            else:
                await advisor.calculate_and_show_profile()
            return

        # Handle education mode
        if advisor.current_mode == "education":
            await advisor.handle_education_mode(msg)
            return

        # Handle unexpected states
        await cl.Message(
            content="I'm not sure how to proceed. Let's start over.\n\n"
                   "1. Learn about investments and the JSE\n"
                   "2. Create a personalized investment profile\n\n"
                   "Please select 1 or 2 to proceed."
        ).send()
        advisor.reset_state()

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        advisor.reset_state()
        await cl.Message(
            content="I apologize, but I encountered an error. Let's start over.\n\n"
                   "1. Learn about investments and the JSE\n"
                   "2. Create a personalized investment profile\n\n"
                   "Please select 1 or 2 to proceed."
        ).send()

@cl.on_chat_end
async def end():
    """Clean up on chat end"""
    advisor.reset_state()

if __name__ == "__main__":
    cl.run()
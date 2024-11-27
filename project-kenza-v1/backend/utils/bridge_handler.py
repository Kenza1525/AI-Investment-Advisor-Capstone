import chainlit as cl

class BridgeHandler:
    def __init__(self):
        pass

    async def update_form_field(self, field: str, value: str):
        """Update a single form field in the dashboard"""
        try:
            await cl.Message(
                content=f"Updating form field {field} with value: {value}"
            ).send()
            await cl.Message(
                content=f"Updating form field {field} with value: {value}"
            ).send()
        except Exception as e:
            print(f"Error updating form field: {str(e)}")

    async def update_chart(self, profile_data: dict):
        """Update the chart visualization in the dashboard"""
        try:
            copilot = cl.CopilotFunction(name="update_chart", args=profile_data)
            res = await copilot.acall()
            await cl.Message(
                content=f"Updating chart with profile data: {profile_data}"
            ).send()
        except Exception as e:
            print(f"Error updating chart: {str(e)}")


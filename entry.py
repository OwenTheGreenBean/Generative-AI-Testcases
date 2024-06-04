import asyncio
import copilot_calls

class Entry:
    def __init__(self, entry_ID, description, requirment):
        self.ID = entry_ID
        self.Description = description
        self.Requirment = requirment
        self.Prompt = "Write me a test case for the following requirement " + requirment + ' in the following format using short sentances: "Test steps: " "Test Rationale: " "Sample Size: " and "Sample Size Rationale: "'
        self.Response = "No Response Generated"
        self.Status = "imported"

    def set_Status(self, input_status):
        self.Status = input_status

    async def generate_text(self):
        self.Response = await copilot_calls.get_sydney_response(self.Prompt)
        self.Status = "Generated"

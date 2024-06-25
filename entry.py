import asyncio
import copilot_calls

class Entry:

    def __init__(self, entry_ID, description, requirment):
        self.ID = entry_ID
        self.Description = description
        self.Requirment = requirment
        self.Prompt = "Write me a test case for the following requirement " + requirment + ' in the following format: '
        self.Response = "No Response Generated"
        self.Status = "imported"

#pretty self explanitory.
    def set_Status(self, input_status):
        self.Status = input_status
#generates text for a single prompt and then stores the response in the response varaible this updates the status to then
# have the status read by the windows file.
    async def generate_text(self):
        self.Response = await copilot_calls.get_ai_response(self.Prompt)
        self.Status = "Generated"


    def change_prompt(self, req, add):
        if add:
            if req not in self.Prompt:
            # Add string to the prompt
                self.Prompt += req
        else:
            # Remove string from the prompt
            self.Prompt = self.Prompt.replace(req, '')
        print(self.Prompt)
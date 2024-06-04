from sydney import SydneyClient

async def get_sydney_response(input_text: str) -> str:
    async with SydneyClient(style="precise") as sydney:
        response_text = ""
        async for response in sydney.ask_stream(input_text, citations=False):
            response_text += response
        return response_text



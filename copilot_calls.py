import google.generativeai as genai
import os

async def get_sydney_response(input_text: str) -> str:
    genai.configure(api_key = "AIzaSyCpGCkz0_95VX7Emcuo_G1OFgcnet1xuwU") 

    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(input_text)
    return response.text



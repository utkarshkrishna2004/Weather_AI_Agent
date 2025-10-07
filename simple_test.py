# Example usage of Gemini API and wttr.in API before building full agent


import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The Current Weather conditions in {city.capitalize()} are {response.text}"
    
    return "Something went wrong..."

def main():
    user_query = input("> ")
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "user", "content": user_query}
        ]
    )

    print(f"🤖: {response.choices[0].message.content}")

print(get_weather("calcutta"))


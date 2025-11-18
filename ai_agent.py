from google import genai
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Get Discord bot token and channel ID from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

def send_message(content: str):
    url = f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    json_data = {
        "content": content
    }

    resp = requests.post(url, headers=headers, json=json_data)
    if resp.status_code == 200 or resp.status_code == 201:
        print("Successfully sent message: ", resp.json()["id"])
    else:
        print("Failed to send message: ", resp.status_code, resp.text)




if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY didn't set in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

send_message(response.text)
print(response.text)
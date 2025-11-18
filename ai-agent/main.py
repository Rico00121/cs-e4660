from google import genai
from dotenv import load_dotenv
import os
from discord_service import send_message, send_alert_embed_card

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY didn't set in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

send_message(response.text)
send_alert_embed_card(
    title="[ALERT] Temperature High",
    description="ColdRoom #3 temperature exceeded threshold",
    fields={"Current Temp": "-2°C", "Threshold": "-5°C"},
    level="warning",
)
print(response.text)
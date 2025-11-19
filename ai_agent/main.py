from google import genai
from dotenv import load_dotenv
import os
from prompt import SYSTEM_PROMPT
from discord_service import send_message, send_embed_card
from loki_service import query_loki_logs
# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY didn't set in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

logs = query_loki_logs(minutes=1, label_match="{service=\"cloud\"}")

logs_text = ""
for log in logs[:5]:  # Take the last 5 logs to avoid too long
    logs_text += log['line'] + "\n"

print(logs_text)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=logs_text,
    config={
        "system_instruction": SYSTEM_PROMPT,
    }
)

send_message(response.text)
send_embed_card(
    title="[ALERT] Temperature High",
    description="ColdRoom #3 temperature exceeded threshold",
    fields={"Current Temp": "-2°C", "Threshold": "-5°C"},
    level="warning",
)
print(response.text) 
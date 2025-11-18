from dotenv import load_dotenv
import os
import requests


# Load environment variables from .env file
load_dotenv()

# Get Discord bot token and channel ID from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_FAILURE_CHANNEL_ID = os.getenv("DISCORD_FAILURE_CHANNEL_ID")
DISCORD_GENERAL_CHANNEL_ID = os.getenv("DISCORD_GENERAL_CHANNEL_ID")
def send_message(content: str):
    url = f"https://discord.com/api/v10/channels/{DISCORD_GENERAL_CHANNEL_ID}/messages"
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

def send_embed_card(
    title: str,
    description: str,
    fields: dict | None = None,
    level: str = "warning",
):
    """
    Send an alert embed card to the Discord channel.

    :param title: The title of the embed card, like "[ALERT] Temperature High"
    :param description: The description of the embed card, like "ColdRoom #3 temperature exceeded threshold"
    :param fields: The extra fields, dict format, like {"Current Temp": "-2°C", "Threshold": "-5°C"}
    :param level: The alert level, optional "info" / "warning" / "critical"
    """

    # Different levels use different colors (16-bit integer)
    level_colors = {
        "info": 0x3498DB,      # Blue
        "warning": 0xF1C40F,   # Yellow
        "critical": 0xE74C3C,  # Red
    }
    color = level_colors.get(level, 0xF1C40F)

    url = f"https://discord.com/api/v10/channels/{DISCORD_FAILURE_CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    embed = {
        "title": title,
        "description": description,
        "color": color,
    }

    # Convert the fields dict to the format required by Discord
    if fields:
        embed["fields"] = [
            {
                "name": str(k),
                "value": str(v),
                "inline": True
            }
            for k, v in fields.items()
        ]

    json_data = {
        "embeds": [embed]
    }

    resp = requests.post(url, headers=headers, json=json_data)
    if resp.status_code in (200, 201):
        print("Successfully sent alert embed card: ", resp.json()["id"])
    else:
        print("Failed to send alert embed card: ", resp.status_code, resp.text)

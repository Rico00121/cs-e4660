from openai import OpenAI
from dotenv import load_dotenv
import os
from prompt import SYSTEM_PROMPT
from discord_service import send_embed_card
from loki_service import query_loki_logs
from pydantic import BaseModel, Field
from typing import Optional, Dict

# Define the response schema using Pydantic
class AnalysisResult(BaseModel):
    status: str = Field(description="Status of the system: 'normal', 'warning', or 'critical'")
    summary: str = Field(description="Brief summary of the analysis")
    description: str = Field(description="Detailed description of the situation")
    anomalies: Optional[Dict[str, str]] = Field(default=None, description="Dictionary of anomaly details, e.g., {'Room': 'ColdRoom #3', 'Current Temp': '-2°C'}")

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY didn't set in .env file")

client = OpenAI(api_key=OPENAI_API_KEY)

logs = query_loki_logs(minutes=1, label_match="{service=\"cloud\"}")

logs_text = ""
for log in logs[:5]:  # Take the last 5 logs to avoid too long
    logs_text += log['line'] + "\n"

print("Using the following logs for analysis...")
print(logs_text)

completion = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": logs_text},
    ],
    response_format=AnalysisResult,
)

result = completion.choices[0].message.parsed

print(f"Parsed result: {result}")

# Process the result
status = result.status.lower()

# Send periodic analysis result to general channel
send_embed_card(
    title="Periodic AI Analysis Result",
    description=f"Status: {result.status}\n{result.summary}",
    level="info",
)

# Only send alert embed card when status is critical or warning
if status in ["critical", "warning"]:
    # Extract anomalies field as fields
    fields = {}
    if result.anomalies:
        fields = {k: str(v) for k, v in result.anomalies.items()}
    
    # Send embed card to failure channel
    send_embed_card(
        title=f"[{status.upper()}] {result.summary}",
        description=result.description,
        fields=fields,
        level=status  # "critical" or "warning"
    )
    print(f"Alert sent: {status}")
else:
    print(f"Status is {status}, no alert sent") 
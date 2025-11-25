from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from ai_agent.prompt import SYSTEM_PROMPT
from ai_agent.discord_service import send_embed_card
from ai_agent.loki_service import query_loki_logs
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


def analyze_logs(minutes: int = 1, log_limit: Optional[int] = None, send_to_discord: bool = True) -> Dict:
    """
    Analyze logs with configurable parameters for QoA experiments.
    
    Args:
        minutes: Time range to query logs (in minutes)
        log_limit: Number of logs to analyze, if None, all logs will be analyzed
        send_to_discord: Whether to send results to Discord
    
    Returns:
        Dictionary containing analysis result and metrics
    """
    start_time = time.time()
    
    # Query logs from Loki
    logs = query_loki_logs(minutes=minutes, label_match="{service=\"cloud\"}")
    
    # Limit log count
    if log_limit is None:
        logs_to_analyze = logs
    else:
        logs_to_analyze = logs[:log_limit]
    
    logs_text = ""
    for log in logs_to_analyze:
        logs_text += log['line'] + "\n"
    
    # Call OpenAI API
    api_start = time.time()
    completion = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": logs_text},
        ],
        response_format=AnalysisResult,
    )
    api_time = time.time() - api_start
    
    result = completion.choices[0].message.parsed
    total_time = time.time() - start_time
    
    # Extract device count from logs 
    device_ids = set()
    for log in logs_to_analyze:
        if 'device_id' in log['line']:
            parts = log['line'].split('device_id')
            if len(parts) > 1:
                device_ids.add(parts[1][:10]) 
    
    metrics = {
        "time_range_minutes": minutes,
        "log_limit": log_limit,
        "log_count": len(logs_to_analyze),
        "total_logs_available": len(logs),
        "device_count": len(device_ids),
        "analysis_time_seconds": round(total_time, 2),
        "api_time_seconds": round(api_time, 2),
        "status": result.status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Send to Discord if enabled
    if send_to_discord:
        status = result.status.lower()
        
        # Send periodic analysis result to general channel
        send_embed_card(
            title="Periodic AI Analysis Result",
            description=f"Status: {result.status}\n{result.summary}",
            level="info",
        )
        
        # Only send alert embed card when status is critical or warning
        if status in ["critical", "warning"]:
            fields = {}
            if result.anomalies:
                fields = {k: str(v) for k, v in result.anomalies.items()}
            
            send_embed_card(
                title=f"[{status.upper()}] {result.summary}",
                description=result.description,
                fields=fields,
                level=status
            )
    
    return {
        "result": result,
        "metrics": metrics
    }


# Main execution - using default parameters (for backward compatibility)
if __name__ == "__main__":
    # Teacher's questions to explore:
    # 1. more data or less data? behavior change?
    # 2. QoA time, accuracy, number of devices? why?
    # 3. try to extend the time range, behavior change? correct?
    
    # Default execution with current settings
    analyze_logs(minutes=1, log_limit=5, send_to_discord=True) 
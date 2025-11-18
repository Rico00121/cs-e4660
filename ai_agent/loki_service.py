import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

LOKI_URL = "http://localhost:3100" 


def _to_ns(ts: datetime) -> int:
    """datetime -> unix ns"""
    return int(ts.timestamp() * 1e9)


def query_loki_logs(
    label_match: str,
    minutes: int = 1,
    limit: int = 1000,
) -> List[Dict[str, Any]]:
    """
    Fetch the latest N minutes of logs from Loki.

    :param label_match: The `{...}` part of LogQL, like `{service="neuronex"}`
    :param minutes: The number of minutes to look back, e.g. 1 means the last 1 minute
    :param limit: The maximum number of logs to return
    :return: The log list, each is a dict, containing timestamp and line
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes)

    start_ns = _to_ns(start)
    end_ns = _to_ns(now)

    query = label_match  # For example '{service="neuronex"}'

    params = {
        "query": query,
        "start": str(start_ns),
        "end": str(end_ns),
        "limit": str(limit),
        "direction": "backward",  # New logs are at the front
    }

    url = f"{LOKI_URL}/loki/api/v1/query_range"
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    # Loki return structure: data -> result (list of streams)
    # Each stream: { "stream": {...labels...}, "values": [[timestamp_ns_str, line_str], ...] }
    logs: List[Dict[str, Any]] = []

    for stream in data.get("data", {}).get("result", []):
        stream_labels = stream.get("stream", {})
        for ts_ns, line in stream.get("values", []):
            logs.append(
                {
                    "timestamp_ns": int(ts_ns),
                    "timestamp": datetime.fromtimestamp(int(ts_ns) / 1e9, tz=timezone.utc),
                    "line": line,
                    "labels": stream_labels,
                }
            )

    # Here you can sort the logs by time (optional)
    logs.sort(key=lambda x: x["timestamp_ns"], reverse=True)
    return logs

if __name__ == "__main__":
    logs = query_loki_logs(minutes=1, label_match="{service=\"cloud\"}")
    for log in logs[:5]:
        print(log["line"])  

from fastapi import FastAPI
from contextlib import asynccontextmanager
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "device/status"

def on_connect(client, userdata, flags, rc):
    """Connection callback"""
    if rc == 0:
        print(f"✓ Connected to {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"✓ Subscribed to topic: {MQTT_TOPIC}\n")

def on_message(client, userdata, msg):
    """Message callback"""
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {msg.topic}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("-" * 50)
    except:
        print(f"{msg.topic}: {msg.payload.decode('utf-8')}")

# MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/Shutdown"""
    print("=== Cloud Service Starting ===")
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    yield
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("\n=== Cloud Service Stopped ===")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"service": "Cloud Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)


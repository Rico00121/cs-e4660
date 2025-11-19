from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import random, time

app = FastAPI()

class ScenarioType(str, Enum):
    """Scenario types"""
    NORMAL = "normal"  # Normal operation
    COOLING_FAILURE = "cooling_failure"  # Cooling failure

class ColdRoomStatus(BaseModel):
    device_id: str
    timestamp: int
    temp_c: float
    door_open: int
    compressor_current_a: float
    setpoint_c: float

class MockColdRoom:
    """Mock cold room device"""
    def __init__(self, device_id: str, setpoint_c: float = 4.0):
        self.device_id = device_id
        self.setpoint_c = setpoint_c
        self.scenario = ScenarioType.NORMAL  # Default to normal scenario
        self.door_open = 0
        self.temp_c = 4.0
        self.compressor_current_a = 5.0

    def get_status(self) -> ColdRoomStatus:
        """Get current status (generate data based on scenario)"""
        if self.scenario == ScenarioType.NORMAL:
            # Scenario 1: Normal operation
            # Door occasionally opens (20% probability)
            self.door_open = 1 if random.random() < 0.2 else 0
            
            # Temperature stable around setpoint (3.5-5.0°C)
            # Slightly higher if door is open
            if self.door_open == 1:
                self.temp_c = round(random.uniform(4.5, 5.5), 2)
            else:
                self.temp_c = round(random.uniform(3.5, 5.0), 2)
            
            # Compressor current normal range (4.8-5.6A)
            self.compressor_current_a = round(random.uniform(4.8, 5.6), 2)
            
        elif self.scenario == ScenarioType.COOLING_FAILURE:
            # Scenario 2: Cooling failure
            # Door always closed
            self.door_open = 0
            
            # Temperature consistently above setpoint (8-12°C)
            self.temp_c = round(random.uniform(8.0, 12.0), 2)
            
            # Compressor current high (6.0-6.8A) - indicating abnormal load
            self.compressor_current_a = round(random.uniform(6.0, 6.8), 2)
        
        return ColdRoomStatus(
            device_id=self.device_id,
            timestamp=int(time.time()),
            temp_c=self.temp_c,
            door_open=self.door_open,
            compressor_current_a=self.compressor_current_a,
            setpoint_c=self.setpoint_c,
        )
    
    def set_scenario(self, scenario: ScenarioType) -> dict:
        """Switch scenario"""
        self.scenario = scenario
        return {
            "device_id": self.device_id,
            "scenario": self.scenario.value,
            "message": f"Scenario switched to: {self.scenario.value}"
        }
    

# Create global cold room instance
cold_room = MockColdRoom(device_id="A1", setpoint_c=4.0)

# ========== API Endpoints ==========

@app.get("/status", response_model=ColdRoomStatus)
def get_status():
    """Get device status"""
    data = cold_room.get_status()
    print(f'[Simulator device {data.device_id}] API called - temp: {data.temp_c}°C, door: {data.door_open}, current: {data.compressor_current_a}A')
    return data

@app.get("/scenario/normal")
def set_normal_scenario():
    """Switch to scenario 1: Normal operation"""
    result = cold_room.set_scenario(ScenarioType.NORMAL)
    print(f"Scenario switched: {result}")
    return result

@app.get("/scenario/cooling-failure")
def set_cooling_failure_scenario():
    """Switch to scenario 2: Cooling failure"""
    result = cold_room.set_scenario(ScenarioType.COOLING_FAILURE)
    print(f"Scenario switched: {result}")
    return result

@app.get("/scenario/current")
def get_current_scenario():
    """Get current scenario"""
    return {
        "device_id": cold_room.device_id,
        "scenario": cold_room.scenario.value,
        "description": "Normal operation" if cold_room.scenario == ScenarioType.NORMAL else "Cooling failure"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
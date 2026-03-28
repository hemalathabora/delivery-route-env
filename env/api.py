from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import DeliveryEnv
from tasks.easy import get_task

app = FastAPI()

env = None

class Action(BaseModel):
    target: int

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/reset")
def reset():
    global env
    try:
        env = DeliveryEnv(get_task())
        return env.reset()
    except Exception as e:
        return {"error": str(e)}

@app.post("/step")
def step(action: Action):
    try:
        state, reward, done = env.step({"target": action.target})
        return {
            "state": state,
            "reward": reward,
            "done": done
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/state")
def state():
    try:
        return env.state()
    except Exception as e:
        return {"error": str(e)}

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
    return {"message": "Delivery Route Optimizer API is running"}
@app.post("/reset")
def reset():
    global env
    env = DeliveryEnv(get_task())
    return env.reset()

@app.post("/step")
def step(action: Action):
    state, reward, done = env.step({"target": action.target})
    return {
        "state": state,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def state():
    return env.state()
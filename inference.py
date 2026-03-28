import math
from env.environment import DeliveryEnv
from tasks.easy import get_task as easy
from tasks.medium import get_task as medium
from tasks.hard import get_task as hard
from graders.grader import grade

# Utility: Distance calculation
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Smarter Agent Logic
def choose_best_delivery(state):
    current = state["current_location"]
    deliveries = state["pending_deliveries"]

    best = None
    best_score = float("inf")

    for d in deliveries:
        dist = distance(current, d["location"])
        time_left = d["deadline"] - state["time_elapsed"]

        # Avoid division issues
        if time_left <= 0:
            urgency_factor = 100  # very urgent (late)
        else:
            urgency_factor = 1 / time_left

        # balanced scoring
        score = dist + 10 * urgency_factor

        if score < best_score:
            best_score = score
            best = d

    return best
# Run single task
def run_task(task_func):
    env = DeliveryEnv(task_func())
    state = env.reset()

    total_reward = 0
    done = False

    while not done:
        if not state["pending_deliveries"]:
            break

        best_delivery = choose_best_delivery(state)

        action = {"target": best_delivery["id"]}

        state, reward, done = env.step(action)
        total_reward += reward

    return total_reward


# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    tasks = [easy, medium, hard]

    for i, task in enumerate(tasks):
        reward = run_task(task)
        score = grade(reward)

        print(f"Task {i+1}: Reward = {reward:.2f}, Score = {score:.2f}")
import math

class DeliveryEnv:
    def __init__(self, deliveries):
        self.deliveries = deliveries
        self.reset()

    def reset(self):
        self.current_location = (0, 0)
        self.time_elapsed = 0
        self.completed = set()
        return self.state()

    def distance(self, a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def step(self, action):
        target_id = action["target"]

        delivery = None
        for d in self.deliveries:
            if d["id"] == target_id and d["id"] not in self.completed:
                delivery = d
                break

        if delivery is None:
            return self.state(), -5, False

        dist = self.distance(self.current_location, delivery["location"])
        self.time_elapsed += dist
        self.current_location = delivery["location"]

        reward = -dist  # travel cost

        if self.time_elapsed <= delivery["deadline"]:
            reward += 10
        else:
            reward += 2

        self.completed.add(delivery["id"])

        done = len(self.completed) == len(self.deliveries)

        if done:
            reward += 20  # bonus

        return self.state(), reward, done

    def state(self):
        return {
            "current_location": self.current_location,
            "pending_deliveries": [
                d for d in self.deliveries if d["id"] not in self.completed
            ],
            "time_elapsed": self.time_elapsed
        }
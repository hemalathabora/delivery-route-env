def get_task():
    return [
        {"id": i, "location": (i*2 % 10, i*3 % 10), "deadline": 10 + i}
        for i in range(1, 10)
    ]
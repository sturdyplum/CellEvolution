import random


class Food:
    def __init__(self):
        self.x_pos = random.uniform(0, 900)
        self.y_pos = random.uniform(0, 900)
        self.alive = True

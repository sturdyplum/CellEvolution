import random
from math import sqrt


class Predator:

    def __init__(self):
        self.x_pos = random.uniform(0, 100)
        self.y_pos = random.uniform(0, 100)
        self.speed = .5

    def move(self, cells):

        min = 10000000

        found_one = False

        for a in cells:
            if a.alive:
                if (a.x_pos-self.x_pos)*(a.x_pos-self.x_pos) + (a.y_pos-self.y_pos) * (a.y_pos-self.y_pos) < min:
                    min = (a.x_pos-self.x_pos)*(a.x_pos-self.x_pos) + (a.y_pos-self.y_pos) * (a.y_pos-self.y_pos)
                    closest_cell = a
                    found_one = True

        if not found_one:
            return

        if sqrt(min) < 1.0:
            closest_cell.alive = False
        else:
            target_x = closest_cell.x_pos
            target_y = closest_cell.y_pos

            if abs(target_x - self.x_pos) < self.speed:
                self.x_pos = target_x
            elif target_x > self.x_pos:
                self.x_pos += self.speed
            else:
                self.x_pos -= self.speed

            if abs(target_y - self.y_pos) < self.speed:
                self.y_pos = target_y
            elif target_y > self.y_pos:
                self.y_pos += self.speed
            else:
                self.y_pos -= self.speed

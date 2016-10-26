import random
from math import sqrt


class Predator:

    def __init__(self):
        self.x_pos = random.uniform(0, 100)
        self.y_pos = random.uniform(0, 100)
        self.speed = 1

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

            movement_vector = [target_x-self.x_pos, target_y-self.y_pos]
            norm_vec = [movement_vector[0]/sqrt(min), movement_vector[1]/sqrt(min)]
            movement_vector2 = [norm_vec[0] * self.speed, norm_vec[1] * self.speed]

            self.x_pos += movement_vector2[0]
            self.y_pos += movement_vector2[1]

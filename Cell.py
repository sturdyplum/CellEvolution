from math import sin, cos, pi, sqrt
from NeuralNetwork import NeuralNetwork
import numpy
import random


class Cell:

    def __init__(self):
        self.x_pos = random.uniform(0, 100)
        self.y_pos = random.uniform(0, 100)
        self.speed = 1.0
        self.rot_speed = pi/8.0     # replace this later
        self.energy = 200
        self.direction = random.uniform(0, 2*pi)
        self.nn = NeuralNetwork(5, 10, 10, 3)
        self.alive = True
        self.fitness = 0

    def get_inputs(self, food, predators):
        rotated_x1 = .5 * cos(self.direction) - 2 * sin(self.direction)
        rotated_x2 = -.5 * cos(self.direction) - 2 * sin(self.direction)
        rotated_y1 = 2 * cos(self.direction) + .5 * sin(self.direction)
        rotated_y2 = 2 * cos(self.direction) - .5 * sin(self.direction)

        rotated_x1 += self.x_pos
        rotated_x2 += self.x_pos
        rotated_y1 += self.y_pos
        rotated_y2 += self.y_pos

        antenna = [[rotated_x1, rotated_y1], [rotated_x2, rotated_y2]]

        min_food1 = 10000000
        min_pred1 = 10000000

        for a in food:
            tmp = sqrt((antenna[0][0] - a.x_pos) * (antenna[0][0] - a.x_pos) + (antenna[0][1] - a.y_pos) * (antenna[0][1] - a.y_pos))
            if tmp < min_food1:
                min_food1 = tmp

        for a in predators:
            tmp = sqrt((antenna[0][0] - a.x_pos) * (antenna[0][0] - a.x_pos) + (antenna[0][1] - a.y_pos) * (antenna[0][1] - a.y_pos))
            if tmp < min_pred1:
                min_pred1 = tmp

        min_food2 = 10000000
        min_pred2 = 10000000

        for a in food:
            tmp = sqrt((antenna[1][0] - a.x_pos) * (antenna[1][0] - a.x_pos) + (antenna[1][1] - a.y_pos) * (
            antenna[1][1] - a.y_pos))
            if tmp < min_food2:
                min_food2 = tmp

        for a in predators:
            tmp = sqrt((antenna[1][0] - a.x_pos) * (antenna[1][0] - a.x_pos) + (antenna[1][1] - a.y_pos) * (
            antenna[1][1] - a.y_pos))
            if tmp < min_pred2:
                min_pred2 = tmp

        return [1.0/max(.001, min_food1),
                1.0/max(.001, min_food2),
                1.0/max(.001, min_pred1),
                1.0/max(.001, min_pred2),
                self.energy/200.0]

    def move_forward(self, how_much):
        rotated_x = (-1*how_much) * sin(self.direction)
        rotated_y = (1 * how_much) * cos(self.direction)

        self.x_pos += rotated_x
        self.y_pos += rotated_y

        self.x_pos += 100
        self.y_pos += 100

        self.x_pos %= 100
        self.y_pos %= 100

    def rotate_right(self, how_much):
        self.direction += pi * how_much
        self.direction %= 2*pi

    def rotate_left(self, how_much):
        self.direction -= pi * how_much
        self.direction += 2*pi
        self.direction %= 2*pi

    def make_move(self, food, predators):
        inputs = self.get_inputs(food, predators)
        moves = self.nn.query(inputs)

        self.move_forward(moves[0])
        self.rotate_right(moves[1])
        self.rotate_left(moves[2])

    def move(self, foods, predators):
        self.make_move(foods, predators)
        closets_food = 10000000

        for a in foods:
            tmp = sqrt((self.x_pos - a.x_pos) * (self.x_pos - a.x_pos) + (self.y_pos - a.y_pos) * (
                        self.y_pos - a.y_pos))
            if tmp < closets_food:
                closets_food = tmp
                closets_food1 = a

        if closets_food <= .7:
            self.energy += 100
            self.energy %= 200
            self.fitness += 1
            foods.remove(closets_food1)

        self.energy -= 1
        if self.energy < 0:
            self.alive = False
        return -1

    def mix(self, other):
        for a in range(self.nn.inodes):
            for x in range(self.nn.hnodes1):
                r = random.randint(1, 1000)
                if r == 1:
                    self.nn.weights_input_hidden1[x][a] += numpy.random.randn()/10.0
                elif r > 700:
                    self.nn.weights_input_hidden1[x][a] = other.nn.weights_input_hidden1[x][a]

        for a in range(self.nn.hnodes1):
            for x in range(self.nn.hnodes2):
                r = random.randint(1, 1000)
                if r == 1:
                    self.nn.weights_hidden1_hidden2[x][a] += numpy.random.randn() / 10.0
                elif r > 700:
                    self.nn.weights_hidden1_hidden2[x][a] = other.nn.weights_hidden1_hidden2[x][a]

        for a in range(self.nn.hnodes2):
            for x in range(self.nn.onodes):
                r = random.randint(1, 1000)
                if r == 1:
                    self.nn.weights_hidden2_output[x][a] += numpy.random.randn() / 10.0
                elif r > 700:
                    self.nn.weights_hidden2_output[x][a] = other.nn.weights_hidden2_output[x][a]

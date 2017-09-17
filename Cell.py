from math import sin, cos, pi, sqrt
from NeuralNetwork import NeuralNetwork
import numpy
import random
import copy


class Cell:

    def __init__(self, isPred):
        self.x_pos = random.uniform(0, 900)
        self.y_pos = random.uniform(0, 900)
        self.speed = 1.0
        self.rot_speed = pi/8.0     # replace this later
        self.energy = random.randint(150, 200)
        self.direction = random.uniform(0, 2*pi)
        inputCount = 2
        outputCount = 2
        if Cell.useSecondary:
            inputCount += 2
        if Cell.useMemory:
            inputCount += 1
            outputCount += 1
        self.nn = NeuralNetwork(inputCount, 6, 3, outputCount)
        self.alive = True
        self.fitness = 0
        self.age = 0
        self.memory = 0
        self.speed = 0
        self.isPred = isPred
        self.color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

    # Gets the inputs for the neural network based on two antenas and its self.
    def get_inputs(self, food, predators):
        # Determin the location of the two antenas.
        left_antena_x = -3 * cos(self.direction) - .5 * sin(self.direction)
        right_antena_x = 3 * cos(self.direction) - .5 * sin(self.direction)
        left_antena_y = .5 * cos(self.direction) - 3 * sin(self.direction)
        right_antena_y = .5 * cos(self.direction) + 3 * sin(self.direction)

        left_antena_x += self.x_pos
        right_antena_x += self.x_pos
        left_antena_y += self.y_pos
        right_antena_y += self.y_pos

        antenna = [[left_antena_x, left_antena_y], [right_antena_x, right_antena_y]]

        # Determin the closest food and predator for each of the antena and itself.
        min_food_distance_left_antena = 10000000
        min_food_distance_right_antena = 10000000
        min_food_distance_self = 10000000
        min_pred_distance_left_antena = 10000000
        min_pred_distance_right_antena = 10000000
        min_pred_distance_self = 10000000

        inputs = []
        for a in food:
            distance =(antenna[0][0] - a.x_pos)**2 + (antenna[0][1] - a.y_pos)**2
            min_food_distance_left_antena = min(min_food_distance_left_antena, distance)
            distance = (antenna[1][0] - a.x_pos)**2 + (antenna[1][1] - a.y_pos)**2
            min_food_distance_right_antena = min(min_food_distance_right_antena, distance)
            distance = (self.x_pos - a.x_pos)**2 + (self.y_pos - a.y_pos)**2
            min_food_distance_self = min(min_food_distance_self, distance)
        inputs.extend([min_food_distance_self, min_food_distance_left_antena - min_food_distance_right_antena])
        if Cell.useSecondary:
            for a in predators:
                distance =(antenna[0][0] - a.x_pos)**2 + (antenna[0][1] - a.y_pos)**2
                if distance < min_pred_distance_left_antena:
                    min_pred_distance_left_antena = distance
                distance = (antenna[1][0] - a.x_pos)**2 + (antenna[1][1] - a.y_pos)**2
                if distance < min_pred_distance_right_antena:
                    min_pred_distance_right_antena = distance
                distance = (self.x_pos - a.x_pos)**2 + (self.y_pos - a.y_pos)**2
                if distance < min_pred_distance_self:
                    min_pred_distance_self = distance
            inputs.extend([min_pred_distance_self, min_pred_distance_left_antena - min_pred_distance_right_antena])
        if Cell.useMemory:
            inputs.extend([self.memory])
        return inputs

    # Moves the cell foward in the direction it is currently facing.
    def move_forward(self):
        rotated_x = self.speed * cos(self.direction)
        rotated_y = self.speed * sin(self.direction)

        self.x_pos += rotated_x
        self.y_pos += rotated_y

        #if(self.x_pos == 900 or self.x_pos == 0
         #  or self.y_pos == 900 or self.y_pos == 0):
          #  self.alive = False
        #self.x_pos = min(900, self.x_pos)
        #self.x_pos = max(0, self.x_pos)

        #self.y_pos = min(900, self.y_pos)
        #self.y_pos = max(0, self.y_pos)
    # Rotates the cell clockwise.
    def rotate(self, how_much):
        self.direction +=  how_much
        self.direction %= 2*pi
    def logistic(self, L, k, x0, x):
        return L/(1+numpy.exp(-k*(x-x0)))
    # Makes the cells move for a frame.
    def make_move(self, foods, preds):
        inputs = self.get_inputs(foods, preds)
        moves = self.nn.query(inputs)
        self.rotate(moves[0])
        if self.isPred:
            self.speed = 2
        else:
            self.speed = self.logistic(3, .3, 0, moves[1])+.5
        self.move_forward()
        if Cell.useMemory:
            self.memory = moves[2]

    # Simulates the life of the cell for a single cycle.
    def single_cycle(self, foods, preds):
        self.make_move(foods, preds)
        closets_food = 10000000
        self.age += 1
        self.energy -= int(self.speed/3)
        # Check to see if the cell is close enough to eat the nearest food.
        for a in foods:
            tmp = sqrt((self.x_pos - a.x_pos) * (self.x_pos - a.x_pos) + (self.y_pos - a.y_pos) * (
                        self.y_pos - a.y_pos))
            if tmp < closets_food:
                closets_food = tmp
                closets_food1 = a

        if closets_food <= 1.8:
            self.energy += 200
            self.fitness += 1
            foods.remove(closets_food1)

        # Check to see if the cell has enough energy to survive.
        self.energy -= 1 * int(self.age/400)
        if self.energy < 0:
            self.alive = False
        return -1

    # Combines the cell and another to create a new offspring.
    def mix(self, other):
        child = Cell(self.isPred)
        child.nn = copy.deepcopy(self.nn)
        child.color = copy.deepcopy(self.color)
        for a in range(child.nn.inodes):
            for x in range(child.nn.hnodes1):
                r = random.randint(1, 100)
                if r > 50:
                    child.nn.weights_input_hidden1[a][x] = other.nn.weights_input_hidden1[a][x]
                r = random.randint(1, 100)
                if r == 1:
                    child.nn.weights_input_hidden1[a][x] += numpy.random.normal(0.0,1.0)

        for a in range(child.nn.hnodes1):
            for x in range(child.nn.hnodes2):
                r = random.randint(1, 100)
                if r > 50:
                    child.nn.weights_hidden1_hidden2[a][x] = other.nn.weights_hidden1_hidden2[a][x]
                r = random.randint(1, 100)
                if r == 1:
                    child.nn.weights_hidden1_hidden2[a][x] += numpy.random.normal(0.0,1.0)

        for a in range(child.nn.hnodes2):
            for x in range(child.nn.onodes):
                r = random.randint(1, 100)
                if r > 50:
                    child.nn.weights_hidden2_output[a][x] = other.nn.weights_hidden2_output[a][x]
                r = random.randint(1, 100)
                if r == 1:
                    child.nn.weights_hidden2_output[a][x] += numpy.random.normal(0.0,1.0)
        for k in range(len(child.color)):
            r = random.randint(1, 100)
            if r > 50:
                child.color[k] = other.color[k]
            r = random.randint(1, 100)
            if r == 1:
                child.color[k] += int(numpy.random.normal(0, 40))
            if child.color[k] < 0:
                child.color[k] = 0
            if child.color[k] > 255:
                child.color[k] = 255
        return child

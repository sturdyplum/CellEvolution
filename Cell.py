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
        inputCount = 1
        outputCount = 1
        if Cell.useSecondary:
            inputCount *= 2
        if Cell.useMemory:
            inputCount += 1
            outputCount += 1
        if Cell.controlSpeed:
            outputCount += 1
        self.nn = NeuralNetwork(inputCount, 7, 4, outputCount)
        self.alive = True
        self.fitness = 0
        self.age = 0
        self.memory = 0
        self.speed = 2.4
        self.isPred = isPred
        self.color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        self.min_food = None
        self.min_secondary = None

    # Gets the inputs for the neural network based on two antenas and its self.
    def get_inputs(self, food, secondaries):
        # Determin the location of the two antenas.
        left_antena_x = 15 * cos(self.direction-.3)
        right_antena_x = 15 * cos(self.direction+.3)
        left_antena_y = 15 * sin(self.direction-.3)
        right_antena_y = 15 * sin(self.direction+.3)

        left_antena_x += self.x_pos
        right_antena_x += self.x_pos
        left_antena_y += self.y_pos
        right_antena_y += self.y_pos

        antenna = [[left_antena_x, left_antena_y], [right_antena_x, right_antena_y]]

        # Determin the closest food and predator for each of the antena and itself.
        min_food = self.min_food
        min_food_distance = 10000000000
        min_food_distance_left_antena = 10000000000
        min_food_distance_right_antena = 10000000000
        
        inputs = []
        if min_food:
            min_food_distance = (self.x_pos - min_food.x_pos)**2 + (self.y_pos - min_food.y_pos)**2
            min_food_distance_left_antena = (antenna[0][0] - min_food.x_pos)**2 + (antenna[0][1] - min_food.y_pos)**2
            min_food_distance_right_antena = (antenna[1][0] - min_food.x_pos)**2 + (antenna[1][1] - min_food.y_pos)**2
        inputs.extend([min_food_distance_left_antena - min_food_distance_right_antena])
        
        if Cell.useSecondary:
            min_secondary = self.min_secondary
            min_secondary_distance = 10000000000
            min_secondary_distance_left_antena = 10000000000
            min_secondary_distance_right_antena = 10000000000
            if min_secondary:
                min_secondary_distance = (self.x_pos - min_secondary.x_pos)**2 + (self.y_pos - min_secondary.y_pos)**2
                min_secondary_distance_left_antena = (antenna[0][0] - min_secondary.x_pos)**2 + (antenna[0][1] - min_secondary.y_pos)**2
                min_secondary_distance_right_antena = (antenna[1][0] - min_secondary.x_pos)**2 + (antenna[1][1] - min_secondary.y_pos)**2
            inputs.extend([min_secondary_distance_left_antena - min_secondary_distance_right_antena])
        if Cell.useMemory:
            inputs.extend([self.memory])
        return inputs

    # Moves the cell foward in the direction it is currently facing.
    def move_forward(self):
        rotated_x = self.speed * cos(self.direction)
        rotated_y = self.speed * sin(self.direction)
        if self.isPred:
            rotated_x *= .75
            rotated_y *= .75

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
    def make_move(self, foods, secondaries):
        outputPtr = 0
        inputs = self.get_inputs(foods, secondaries)
        moves = self.nn.query(inputs)
        self.rotate(moves[outputPtr])
        outputPtr += 1
        if Cell.controlSpeed:
            self.speed = self.logistic(3, .3, 0, moves[outputPtr])+.5
            outputPtr += 1
        self.move_forward()
        if Cell.useMemory:
            self.memory = moves[outputPtr]
            outputPtr += 1
    def update_closests(self, foods, secondaries, updateExisting):
        if (not self.min_food or not self.min_food.alive) or updateExisting:
            self.min_food = None
            min_distance = 10000000000
            for a in foods:
                distance = (self.x_pos - a.x_pos)**2 + (self.y_pos - a.y_pos)**2
                if distance < min_distance:
                    min_distance = distance
                    self.min_food = a

        if Cell.useSecondary and (updateExisting or (not self.min_secondary or not self.min_secondary.alive)):
            self.min_secondary = None
            min_distance = 10000000000
            for a in secondaries:
                distance = (self.x_pos - a.x_pos)**2 + (self.y_pos - a.y_pos)**2
                if distance < min_distance:
                    min_distance = distance
                    self.min_secondary = a
  
    # Simulates the life of the cell for a single cycle.
    def single_cycle(self, foods, secondaries, iteration):
        self.update_closests(foods, secondaries, (iteration & 7) == 0)
        self.make_move(foods, secondaries)
        self.age += 1
        # self.energy -= int(self.speed/3)
        # Check to see if the cell is close enough to eat the nearest food.
        if self.min_food and (self.min_food.x_pos-self.x_pos)**2+(self.min_food.y_pos-self.y_pos)**2 <= 1.8*1.8:
            self.energy += 200
            self.fitness += 1
            foods.remove(self.min_food)
            self.min_food.alive = False

        

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

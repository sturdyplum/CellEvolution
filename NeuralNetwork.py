#16 input nodes is there food up down left right, is there predator up down left right, distances(normalized)
import numpy
import scipy.special
from random import randint


class NeuralNetwork:

    def __init__(self, inputnodes, hiddennodes, outputnodes, parent1, parent2, is_child):
        if is_child: #if the cell which this network is a children of two other cells then its neural network will be a random combination of its parents networks
            self.inodes = inputnodes
            self.hnodes = hiddennodes
            self.onodes = outputnodes
            self.activation_function = lambda x: scipy.special.expit(x)
            self.tempWIH = []
            self.tempWHO = []
            for i in range(0 , self.hnodes):
                temp_list = []
                for j in range(0, self.inodes):
                    r = randint(1, 2)
                    if r == 1:
                        temp_list.append(parent1.net.weights_input_hidden[i][j])#50% chance of inheriting certain weight from parent 1 and 50% from parent 2
                    else:
                        temp_list.append(parent2.net.weights_input_hidden[i][j])
                self.tempWIH.append(temp_list)
            for i in range(0, self.onodes):
                temp_list = []
                for j in range(0, self.hnodes):
                    r = randint(1, 2)
                    if r == 1:
                        temp_list.append(parent1.net.weights_hidden_output[i][j])
                    else:
                        temp_list.append(parent2.net.weights_hidden_output[i][j])
                self.tempWHO.append(temp_list)
            self.weights_input_hidden = numpy.array(self.tempWIH)
            self.weights_hidden_output = numpy.array(self.tempWHO)
        else: #if not a child then initialize the weights to be randomly selected from normal distribution
            self.inodes = inputnodes
            self.hnodes = hiddennodes
            self.onodes = outputnodes
            self.activation_function = lambda x: scipy.special.expit(x)
            self.weights_input_hidden = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
            self.weights_hidden_output = numpy.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))

    def query(self, inputs_list):#takes in input and outputs which move should be made
        inputs = numpy.array(inputs_list, ndmin=2).T

        hidden_inputs = numpy.dot(self.weights_input_hidden, inputs)

        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = numpy.dot(self.weights_hidden_output, hidden_outputs)

        final_outputs = self.activation_function(final_inputs)

        return final_outputs


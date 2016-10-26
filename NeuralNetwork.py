import numpy
import scipy.special
from random import randint


class NeuralNetwork:

    def __init__(self, inputnodes, hiddennodes1, hiddennodes2, outputnodes):
        self.inodes = inputnodes
        self.hnodes1 = hiddennodes1
        self.hnodes2 = hiddennodes2
        self.onodes = outputnodes
        self.activation_function = lambda x: scipy.special.expit(x)
        self.weights_input_hidden1 = numpy.random.normal(0.0, pow(self.hnodes1, -0.5), (self.hnodes1, self.inodes))
        self.weights_hidden1_hidden2 = numpy.random.normal(0.0, pow(self.hnodes2, -0.5), (self.hnodes2, self.hnodes1))
        self.weights_hidden2_output = numpy.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes2))

    def query(self, inputs_list):  # takes in input and outputs which move should be made
        inputs = numpy.array(inputs_list, ndmin=2).T

        hidden_inputs1 = numpy.dot(self.weights_input_hidden1, inputs)

        hidden_outputs1 = self.activation_function(hidden_inputs1)

        hidden_inputs2 = numpy.dot(self.weights_hidden1_hidden2, hidden_outputs1)

        hidden_outputs2 = self.activation_function(hidden_inputs2)

        final_inputs = numpy.dot(self.weights_hidden2_output, hidden_outputs2)

        final_outputs = self.activation_function(final_inputs)

        return final_outputs


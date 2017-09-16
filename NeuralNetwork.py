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
        self.weights_input_hidden1 = numpy.random.normal(0.0, 1, (self.inodes, self.hnodes1))
        self.weights_hidden1_hidden2 = numpy.random.normal(0.0, 1, (self.hnodes1, self.hnodes2))
        self.weights_hidden2_output = numpy.random.normal(0.0, 1, (self.hnodes2, self.onodes))

    def query(self, inputs_list):  # takes in input and outputs which move should be made
        inputs = numpy.array(inputs_list, ndmin=2).T

        hidden_inputs1 = numpy.dot(numpy.transpose(inputs),self.weights_input_hidden1)

        hidden_outputs1 = self.activation_function(hidden_inputs1)

        hidden_inputs2 = numpy.dot(hidden_outputs1 ,self.weights_hidden1_hidden2)

        hidden_outputs2 = self.activation_function(hidden_inputs2)

        final_inputs = numpy.dot(hidden_outputs2, self.weights_hidden2_output)

        #final_outputs = self.activation_function(final_inputs)
        #print(final_inputs)
        return final_inputs[0]


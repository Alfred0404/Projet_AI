import numpy as np


class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_output = np.random.randn(output_size)

    def load_parameters(
        self, weights_input_hidden, bias_hidden, weights_hidden_output, bias_output
    ):
        self.weights_input_hidden = weights_input_hidden
        self.bias_hidden = bias_hidden
        self.weights_hidden_output = weights_hidden_output
        self.bias_output = bias_output

    def forward(self, inputs):
        hidden = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        hidden = self._activation(hidden)
        output = np.dot(hidden, self.weights_hidden_output) + self.bias_output
        output = self._activation(output)
        return output

    def _activation(self, x):
        return np.maximum(0, x)  # ReLU

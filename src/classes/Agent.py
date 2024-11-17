from classes.NeuralNetwork import SimpleNeuralNetwork
import numpy as np

class Agent:
    def __init__(self, input_size, hidden_size, output_size):
        self.network = SimpleNeuralNetwork(input_size, hidden_size, output_size)
        self.fitness = 0  # Performance de l'agent
        self.best_lap = 0

    def load_agent(
        self,
        weights_input_hidden,
        bias_hidden,
        weights_hidden_output,
        bias_output,
        best_lap,
        fitness,
    ):
        self.network.load_parameters(
            weights_input_hidden, bias_hidden, weights_hidden_output, bias_output
        )
        self.best_lap = best_lap
        self.fitness = fitness

    def mutate(self, mutation_rate=0.1):
        self.network.weights_input_hidden += mutation_rate * np.random.randn(
            *self.network.weights_input_hidden.shape
        )
        self.network.bias_hidden += mutation_rate * np.random.randn(
            *self.network.bias_hidden.shape
        )
        self.network.weights_hidden_output += mutation_rate * np.random.randn(
            *self.network.weights_hidden_output.shape
        )
        self.network.bias_output += mutation_rate * np.random.randn(
            *self.network.bias_output.shape
        )

    def crossover(self, other_agent):
        child = Agent(
            input_size=self.network.weights_input_hidden.shape[0],
            hidden_size=self.network.weights_input_hidden.shape[1],
            output_size=self.network.weights_hidden_output.shape[1],
        )
        child.network.weights_input_hidden = (
            self.network.weights_input_hidden + other_agent.network.weights_input_hidden
        ) / 2
        child.network.bias_hidden = (
            self.network.bias_hidden + other_agent.network.bias_hidden
        ) / 2
        child.network.weights_hidden_output = (
            self.network.weights_hidden_output
            + other_agent.network.weights_hidden_output
        ) / 2
        child.network.bias_output = (
            self.network.bias_output + other_agent.network.bias_output
        ) / 2
        return child

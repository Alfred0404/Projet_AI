import numpy as np

class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialisation des poids et biais
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_output = np.random.randn(output_size)

    def forward(self, inputs):
        # Propagation avant
        hidden = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        hidden = self._activation(hidden)
        output = np.dot(hidden, self.weights_hidden_output) + self.bias_output
        output = self._activation(output)
        return output

    def _activation(self, x):
        # Fonction d'activation (ReLU ou Sigmoïde)
        return np.maximum(0, x)  # ReLU

# Exemple d'initialisation
nn = SimpleNeuralNetwork(input_size=5, hidden_size=16, output_size=3)

# Exemple d'inférence
inputs = np.array([0.5, 1.2, 0.3, 0.7, 1.0])  # Données des rayons
output = nn.forward(inputs)
print("Actions proposées :", output)


class Agent:
    def __init__(self, input_size, hidden_size, output_size):
        self.network = SimpleNeuralNetwork(input_size, hidden_size, output_size)
        self.fitness = 0  # Performance de l'agent

    def mutate(self, mutation_rate=0.1):
        # Modifier les poids et biais aléatoirement
        self.network.weights_input_hidden += mutation_rate * np.random.randn(*self.network.weights_input_hidden.shape)
        self.network.bias_hidden += mutation_rate * np.random.randn(*self.network.bias_hidden.shape)
        self.network.weights_hidden_output += mutation_rate * np.random.randn(*self.network.weights_hidden_output.shape)
        self.network.bias_output += mutation_rate * np.random.randn(*self.network.bias_output.shape)

    def crossover(self, other_agent):
        # Combiner les réseaux de deux agents pour créer un nouvel agent
        child = Agent(
            input_size=self.network.weights_input_hidden.shape[0],
            hidden_size=self.network.weights_input_hidden.shape[1],
            output_size=self.network.weights_hidden_output.shape[1]
        )
        # Mélanger les poids des deux parents
        child.network.weights_input_hidden = (self.network.weights_input_hidden + other_agent.network.weights_input_hidden) / 2
        child.network.bias_hidden = (self.network.bias_hidden + other_agent.network.bias_hidden) / 2
        child.network.weights_hidden_output = (self.network.weights_hidden_output + other_agent.network.weights_hidden_output) / 2
        child.network.bias_output = (self.network.bias_output + other_agent.network.bias_output) / 2
        return child

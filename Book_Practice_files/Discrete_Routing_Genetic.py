import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
# Define the graph
graph = {
    'A': {'B': 4, 'C': 11, 'D': 10 },
    'B': {'A': 4, 'C': 20, 'E': 1},
    'C': {'A': 11, 'B': 20, 'D': 3, 'F': 15},
    'D': {'A': 10, 'C': 3, 'G': 7},
    'E': {'B': 1, 'F': 7, 'H': 30},
    'F': {'C': 15, 'E': 7, 'H': 5, 'G': 2},
    'G': {'D': 7, 'H': 40, 'F': 2},
    'H': {'E': 30, 'F': 5, 'G': 40}
}
# Define the genetic algorithm parameters
population_size = 500
num_generations = 1000
mutation_rate = 0.3
source='A'
destination='H'
# Define the fitness function
def fitness(path):
    total_distance = 0
    # a valid path should start from source
    if source!=path[0]:
        return float('inf')
    if  path[-1] !=destination:
        return float('inf')    
    # check connectivity of path
    for i in range(len(path)-1):
        node1 = path[i]
        node2 = path[i + 1]
        if node2 in graph[node1]:
            total_distance += graph[node1][node2]
        else:
            return float('inf')
    return 1 / total_distance
# Define the crossover function
def crossover(parent1, parent2):
    child = []
    used_nodes = set()
    for i in range(len(parent1)):
        if random.random() < 0.5:
            node = parent1[i]
        else:
            if i < len(parent2):
                node = parent2[i]
            else:
                node = parent1[i]
        if node not in used_nodes:
            child.append(node)
            used_nodes.add(node)
    return child
# Define the mutation function
def mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual
# Define the genetic algorithm
def genetic_algorithm():
    # Initialize the population
    population = [list(graph.keys())[i:] + list(graph.keys())[:i] for i in range(len(graph))]
    best_fitness=float('inf')
    best_solution=None
    random.shuffle(population)
    # Evolve the population
    for generation in range(num_generations):
        # Evaluate the fitness of each individual
        fitness_values = [fitness(individual) for individual in population]
        # Select the best individuals for reproduction
        parents = [population[i] for i in np.argsort(fitness_values)[:population_size // 2]]
        parents2 = [population[i] for i in np.argsort(fitness_values)[:]]
        # Create the next generation
        new_population = parents[:]
        while len(new_population) < population_size:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        #  the best individual in current generation
        fitness_values = [fitness(individual) for individual in population]
        best_index = np.argmin(fitness_values)
        if fitness_values[best_index]<best_fitness:
            best_solution=population[best_index]
            best_fitness=fitness_values[best_index]
        # Update the population for next generation
        population = new_population
    return best_solution,best_fitness
# Run the genetic algorithm
best_path , result= genetic_algorithm()
if result==float('inf'):
    print("There is no Valid path in my Solution")
else:
    print("Best path:", " -> ".join(best_path))
    print(" Cost=",1/result)


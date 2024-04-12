import random
import numpy as np
import matplotlib.pyplot as plt

# Define the cost and delay graphs
cost = {
    'A': {'B': 4, 'C': 11, 'D': 20},
    'B': {'C': 20, 'E': 1, 'A': 4},
    'C': {'D': 3, 'F': 15, 'A': 11, 'B': 20},
    'D': {'G': 7, 'A': 20, 'C': 3},
    'E': {'H': 30, 'F': 7, 'B': 1},
    'H': {'F': 5, 'E': 30, 'G': 40},
    'F': {'H': 5, 'G': 2, 'C': 15, 'E': 7},
    'G': {'H': 40, 'D': 7, 'F': 2},
}

delay = {
    'A': {'B': 5, 'C': 11, 'D': 2},
    'B': {'C': 20, 'E': 1, 'A': 5},
    'C': {'D': 13, 'F': 25, 'A': 11, 'B': 20},
    'D': {'G': 17, 'A': 2, 'C': 13},
    'E': {'H': 3, 'F': 17, 'B': 1},
    'H': {'F': 5, 'E': 3, 'G': 4},
    'F': {'H': 3, 'G': 2, 'C': 25, 'E': 17},
    'G': {'H': 4, 'D': 17, 'F': 2},
}

# Define the genetic algorithm parameters
population_size = 1006
num_generations = 1
mutation_rate = 0.3
source='A'
destination='F'
# Define the fitness functions
def cost_fitness(path):
    total_cost = 0
    # a valid path should start from source
    if source!=path[0]:
        return float('inf')
    if  path[-1] !=destination:
        return float('inf')    
    # check connectivity of path
    for i in range(len(path)-1):
        node1 = path[i]
        node2 = path[i + 1]
        if node2 in cost[node1]:
            total_cost += cost[node1][node2]
        else:
            return float('inf')
    return 1 / total_cost

def delay_fitness(path):
    total_delay = 0
    # a valid path should start from source
    if source!=path[0]:
        return float('inf')
    if  path[-1] !=destination:
        return float('inf')    
    # check connectivity of path
    for i in range(len(path)-1):
        node1 = path[i]
        node2 = path[i + 1]
        if node2 in delay[node1]:
            total_delay += delay[node1][node2]
        else:
            return float('inf')
    return 1 / total_delay

# Define the non-dominated sorting function
def non_dominated_sort(population):
    fronts = []
    inside_pop={}
    inside_pop2=[]
    index=0
    for item in population:
        inside_pop[index]={}
        if item[1]!=float('inf') and item[2]!=float('inf'):
             inside_pop[index]=(item[1],item[2])
             inside_pop2.append([item[1],item[2]])
             index=index+1
    print(inside_pop)
    inside_pop2 = np.array(inside_pop2)
    print(inside_pop2)
    # Find the non-dominated fronts
    for individual in population:
        dominated_count = 0
        dominated_solutions = []
        if individual[1]!=float('inf') and individual[2]!=float('inf'): #cancel invalid solution
            for other in population:
                if other[1]!=float('inf') and other[2]!=float('inf'):#cancel invalid solution
                     # individual that they dominate me (I am bigger than them)
                    if (individual[1] <= other[1] and individual[2] <= other[2] and
                        (individual[1] < other[1] or individual[2] < other[2])):
                        dominated_count += 1#sub
                        #print(individual)
                        # individual that I dominate them (I am smaller than them)
                    elif (individual[1] >= other[1] and individual[2] >= other[2] and 
                        (individual[1] > other[1] or individual[2] > other[2])):
                        dominated_solutions.append(other)#add
            if dominated_count == 0:
                fronts.append([individual])

    #if len(dominated_solutions)>0:
            #print(dominated_solutions,"++++")
    #print(fronts,"****",len(population))
    #print(dominated_solutions,"---",len(dominated_solutions))
    # Calculate the crowding distance for each solution
    crowding_distances = [0] * len(population)
    #print(crowding_distances)
    for front in fronts:
        for i in range(len(front)):
            front[i].append(crowding_distances[population.index(front[i])])
        #print("**",front)
        front.sort(key=lambda x: x[2], reverse=True)
        #print("+++",front)
        crowding_distances[population.index(front[0])] = float('inf')
        crowding_distances[population.index(front[-1])] = float('inf')
        for i in range(1, len(front) - 1):
            crowding_distances[population.index(front[i])] += (
                front[i + 1][1] - front[i - 1][1]) / (
                    max(front[1] ,front[1]) -min(front[1] , [1]))
    #print("+",fronts)
    return fronts

# Define the crossover and mutation functions
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

def mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

# Define the NSGA-II algorithm
def nsga2(): 

    # Evolve the population
    for generation in range(num_generations):
            # Initialize the population
        population = [list(cost.keys())[i:] for i in range(len(cost))]
        population=[]
        for i in range(population_size):
            path_len=random.randint(1,len(cost))
            path=[]
            for j in range(path_len):
                item=random.randint(0,len(cost)-1)
                if list(cost.keys())[item]!=source and list(cost.keys())[item]!=destination and list(cost.keys())[item] not in path:
                    path.append(list(cost.keys())[item])
            population.append(path)
        random.shuffle(population)
        for p in population:
            if source in p:
                p.remove(source)
            if destination in p:
                p.remove(destination)
            p.insert(0,source)
            p.insert(len(p),destination) 
        # Evaluate the fitness of each individual
        population_with_fitness2 = []
        population_with_fitness = [[individual] + [cost_fitness(individual), delay_fitness(individual)] for individual in population]
        d=1

        for i in population_with_fitness:
            #print(i[0],i[1],i[2])
            if i[1]!=float('inf') and i[2]!=float('inf'):
                population_with_fitness2.append(i)
                d=d+1
            if d>=5:
                break 
        #print(population_with_fitness2)
        # Find the non-dominated fronts
        population_with_fitness=population_with_fitness2
        fronts = non_dominated_sort(population_with_fitness)
        #print("-",fronts)
        # Select the best individuals for the next generation
        new_population = []
        for front in fronts:
            new_population.extend(front[:len(front[0]) // 2])
            #print(len(new_population)," ",front[:len(front) // 2],front,len(front[0]))
        while len(new_population) < population_size:
            if len(new_population) >= 2:
                parent1 = random.choice(new_population)
                parent2 = random.choice(new_population)
                child = crossover(parent1[0], parent2[0])
                child = mutate(child)
                new_population.append(child)
            else:
                break

        # Update the population
        population = new_population

    # Return the non-dominated fronts
    #population_with_fitness = [[individual] + [cost_fitness(individual), delay_fitness(individual)] for individual in population]
    #fronts = non_dominated_sort(population_with_fitness)
    #print(fronts)
    return fronts
def genetic_algorithm():
    # Initialize the population
    population = [list(cost.keys())[i:] + list(cost.keys())[:i] for i in range(len(cost))]
    best_fitness=float('inf')
    best_solution=None
    random.shuffle(population)
    # Evolve the population
    for generation in range(num_generations):
        # Evaluate the fitness of each individual
        fitness_values = [cost_fitness(individual) for individual in population]
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
        fitness_values = [cost_fitness(individual) for individual in population]
        best_index = np.argmin(fitness_values)
        if fitness_values[best_index]<best_fitness:
            best_solution=population[best_index]
            best_fitness=fitness_values[best_index]
        # Update the population for next generation
        population = new_population
    return best_solution,best_fitness




# Run the NSGA-II algorithm
fronts = nsga2()
#print("Result=",fronts)
# Plot the Pareto front
plt.figure(figsize=(8, 6))
for front in fronts:
    costs = [individual[1] for individual in front]
    delays = [individual[2] for individual in front]
    plt.scatter(costs, delays, color='b')
plt.xlabel('Cost')
plt.ylabel('Delay')
plt.title('Pareto Front')
#plt.show()

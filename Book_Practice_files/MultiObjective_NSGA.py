import random
import numpy as np
import matplotlib.pyplot as plt
import functools
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
population_size = 50
num_generations = 200
mutation_rate = 0.3
source='A'
destination='G'
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
def convert_to_array(population):
    inside_pop=[]
    for item in population:
        if item[1]!=float('inf') and item[2]!=float('inf'):
             inside_pop.append([item[1],item[2]])
    inside_pop = np.array(inside_pop)
    return inside_pop
def dominates(fitnesses_1,fitnesses_2):
    # fitnesses_1 is a array of objectives of solution 1 [objective1, objective2 ...]
    larger_or_equal = fitnesses_1 >= fitnesses_2
    larger = fitnesses_1 > fitnesses_2
    if np.all(larger_or_equal) and np.any(larger):
        return True
    return False    
def calculate_pareto_fronts(fitnesses):
    # Calculate dominated set for each individual
    domination_sets = []
    domination_counts = []
    for fitnesses_1 in fitnesses:
        current_dimination_set = set()
        domination_counts.append(0)
        for i,fitnesses_2 in enumerate(fitnesses):
            if dominates(fitnesses_1,fitnesses_2):
                current_dimination_set.add(i)
            elif dominates(fitnesses_2,fitnesses_1):
                domination_counts[-1] += 1
        domination_sets.append(current_dimination_set)
    domination_counts = np.array(domination_counts)
    fronts = []
    while True:
        current_front = np.where(domination_counts==0)[0]
        if len(current_front) == 0:
            break
        fronts.append(current_front)
        for individual in current_front:
            # this individual is already accounted for, make it -1 so  ==0 will not find it anymore
            domination_counts[individual] = -1 
            dominated_by_current_set = domination_sets[individual]
            for dominated_by_current in dominated_by_current_set:
                domination_counts[dominated_by_current] -= 1
    return fronts

def calculate_crowding_metrics(fitnesses,fronts):
    num_objectives = fitnesses.shape[1]
    num_individuals = fitnesses.shape[0]
    # Normalise each objectives, so they are in the range [0,1]
    # This is necessary, so each objective's contribution have the same magnitude to the crowding metric.
    normalized_fitnesses = np.zeros_like(fitnesses)
    for objective_i in range(num_objectives):
        min_val = np.min(fitnesses[:,objective_i])
        max_val = np.max(fitnesses[:,objective_i])
        val_range = max_val - min_val
        normalized_fitnesses[:,objective_i] = (fitnesses[:,objective_i] - min_val) / val_range    
    fitnesses = normalized_fitnesses
    crowding_metrics = np.zeros(num_individuals)
    for front in fronts:
        for objective_i in range(num_objectives):
            sorted_front = sorted(front,key = lambda x : fitnesses[x,objective_i])
            crowding_metrics[sorted_front[0]] = np.inf
            crowding_metrics[sorted_front[-1]] = np.inf
            if len(sorted_front) > 2:
                for i in range(1,len(sorted_front)-1):
                    crowding_metrics[sorted_front[i]] += fitnesses[sorted_front[i+1],objective_i] - fitnesses[sorted_front[i-1],objective_i]
    return  crowding_metrics
def fronts_to_nondomination_rank(fronts):
    nondomination_rank_dict = {}
    for i,front in enumerate(fronts):
        for x in front:   
            nondomination_rank_dict[x] = i
    return nondomination_rank_dict
def nondominated_sort(nondomination_rank_dict,crowding):
    num_individuals = len(crowding)
    indicies = list(range(num_individuals))
    def nondominated_compare(a,b):
        # returns 1 if a dominates b, or if they equal, but a is less crowded
        # return -1 if b dominates a, or if they equal, but b is less crowded
        # returns 0 if they are equal in every sense
        if nondomination_rank_dict[a] > nondomination_rank_dict[b]:  # domination rank, smaller better
            return -1
        elif nondomination_rank_dict[a] < nondomination_rank_dict[b]:
            return 1
        else:
            if crowding[a] < crowding[b]:   # crowding metrics, larger better
                return -1
            elif crowding[a] > crowding[b]:
                return 1
            else:
                return 0
    non_domiated_sorted_indicies = sorted(indicies,key = functools.cmp_to_key(nondominated_compare),reverse=True) # decreasing order, the best is the first
    return non_domiated_sorted_indicies

def non_dominated_sort(population):
    fitnesses=convert_to_array(population)
    fronts = calculate_pareto_fronts(fitnesses)
    nondomination_rank_dict = fronts_to_nondomination_rank(fronts)
    crowding = calculate_crowding_metrics(fitnesses,fronts)
    # Sort the population
    non_domiated_sorted_indicies = nondominated_sort(nondomination_rank_dict,crowding)
    return non_domiated_sorted_indicies
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
def Generate_Initial_Valid_Population():
     # Initialize the population
    Result=[]
    count=0
    while count < population_size:
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
        population_with_fitness = [[individual] + [cost_fitness(individual), delay_fitness(individual)] for individual in population]
        for item in population_with_fitness:
            if item[1]!=float('inf') and item[2]!=float('inf'): # is valid path
                Result.append(item)
                count+=1
    return Result
# Define the NSGA-II algorithm
def nsga2(): 
    population_with_fitness = Generate_Initial_Valid_Population()
    for generation in range(num_generations):
        # Select the best individuals for the next generation
        fronts = non_dominated_sort(population_with_fitness)
        new_population = [population_with_fitness[i] for i in fronts[:len(fronts) // 2]]
        while len(new_population) < population_size:
            if len(new_population) >= 2:
                parent1 = random.choice(new_population)
                parent2 = random.choice(new_population)
                child = crossover(parent1[0], parent2[0])
                child = mutate(child)
                if cost_fitness(child)!=float('inf') and delay_fitness(child)!=float('inf'): #the child is valid solution
                    new_population.append([child] + [cost_fitness(child), delay_fitness(child)])
            else:
                break
        # Update the population
        population_with_fitness = new_population
    return fronts,population_with_fitness
# Run the NSGA-II algorithm
fronts,pop = nsga2()
for front in fronts:
    print("Cost=",pop[front][1] ," Delay=",pop[front][1] ," Path=",pop[front][0]," " ,front)
pop.sort(key=lambda x: x[2], reverse=False)#sort based on delay
pop.sort(key=lambda x: x[1], reverse=False)#sort based on cost
# Plot the Pareto front
plt.figure(figsize=(8, 6))
for front in fronts:
    costs = pop[front][1] 
    delays = pop[front][2] 
    plt.scatter(costs, delays, color='b')
#print Top 3 solution
print(f"Best Answer=",pop[0])    
plt.text(pop[0][1], pop[0][2], f'({pop[0][0]})',fontsize=10) 
plt.xlabel('Cost')
plt.ylabel('Delay')
plt.title('Pareto Front')
plt.show()

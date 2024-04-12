import numpy as np
names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
values = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
weights = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
capacity = 165
# Define the benchmark functions
def knapsack_func(x):
    # Knapsack problem
    return -np.sum([x[i] * values[i] for i in range(len(x))]) if np.sum([x[i] * weights[i] for i in range(len(x))]) <= capacity else np.inf
def knapsack_genetic():
    population_size = 100
    num_generations = 100
    mutation_rate = 0.1
    #10 random int numbers between [0,2)
    population = [np.random.randint(0, 2, 10) for _ in range(population_size)]
    best_value = float('inf')
    best_x = None
    for _ in range(num_generations):
        fitness = [knapsack_func(x) for x in population]
        best_idx = np.argmin(fitness)
        if fitness[best_idx] < best_value:
            best_value = fitness[best_idx]
            best_x = population[best_idx]
        new_population = []
        for _ in range(population_size):
            parent1 = population[np.random.randint(0, population_size)]
            parent2 = population[np.random.randint(0, population_size)]
            child = [parent1[i] if np.random.rand() < 0.5 else parent2[i] for i in range(10)]
            if np.random.rand() < mutation_rate:
                child[np.random.randint(0, 10)] = 1 - child[np.random.randint(0, 10)]
            new_population.append(child)
        population = new_population
    return -best_value,best_x
profit, sol=knapsack_genetic()
if profit!=float('inf'):
    print(f"Genetic algorithm optimal value: {profit}")
    total_weight=0
    total_value=0
    for i in range(len(sol)):
        if sol[i]==1:
            print("Item ", names[i], " value=",values[i]," weight=",weights[i])
            total_value+=values[i]
            total_weight+=weights[i]
    print("Total_Value=",total_value," Total Weight=",total_weight)  
else:
    print("There is no valid Solution")      


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Define the benchmark functions
def sphere(x):
    return np.sum(x**2)

def rosenbrock(x):
    return np.sum(100 * (x[1:] - x[:-1]**2)**2 + (x[:-1] - 1)**2)

def rastrigin(x):
    return 10 * len(x) + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

def ackley(x):
    a = 20
    b = 0.2
    c = 2 * np.pi
    return -a * np.exp(-b * np.sqrt(np.mean(x**2))) - np.exp(np.mean(np.cos(c * x))) + a + np.exp(1)

def griewank(x):
    return 1 + np.sum(x**2 / 4000) - np.prod(np.cos(x / np.sqrt(np.arange(1, len(x) + 1))))

def schwefel(x):
    return 418.9829 * len(x) - np.sum(x * np.sin(np.sqrt(np.abs(x))))

def levy(x):
    d = len(x)
    w = 1 + (x - 1) / 4
    return np.sin(np.pi * w[0])**2 + np.sum((w[:-1] - 1)**2 * (1 + 10 * np.sin(np.pi * w[:-1] + 1)**2)) + (w[-1] - 1)**2 * (1 + np.sin(2 * np.pi * w[-1])**2)

def zakharov(x):
    return np.sum(x**2) + (0.5 * np.sum(x))**2 + (0.5 * np.sum(x))**4

def styblinski_tang(x):
    return 0.5 * np.sum(x**4 - 16 * x**2 + 5 * x)

def michalewicz(x):
    d = len(x)
    return -np.sum(np.sin(x) * np.sin((np.arange(1, d+1)) * x**2 / np.pi)**(2 * 10))

# Solve the benchmark functions using a genetic algorithm
def Compute_Genetic(benchmark_functions):
    results = {}
    for name, func in benchmark_functions.items():
        population_size = 100
        num_generations = 1000
        mutation_rate = 0.1
        population = [np.random.uniform(-10, 10, 10) for _ in range(population_size)]
        best_value = float('inf')
        best_x = None
        for _ in range(num_generations):
            fitness = [func(np.array(x)) for x in population]
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
                    child[np.random.randint(0, 10)] = np.random.uniform(-10, 10)
                new_population.append(child)
            population = new_population
        results[name] = best_value
    return results

# Solve the benchmark functions and store the results
def Compute_Scipy(benchmark_functions):
    results = {}
    for name, func in benchmark_functions.items():
        x0 = np.random.uniform(-10, 10, 10)
        res = minimize(func, x0, method='L-BFGS-B')
        results[name] = res.fun
    return results

# Define the benchmark functions in a dictionary
benchmark_functions = {
    "Sphere": sphere,
    "Rosenbrock": rosenbrock,
    "Rastrigin": rastrigin,
    "Ackley": ackley,
    "Griewank": griewank,
    "Schwefel": schwefel,
    "Levy": levy,
    "Zakharov": zakharov,
    "Styblinski-Tang": styblinski_tang,
    "Michalewicz": michalewicz
}
results_g=Compute_Genetic(benchmark_functions)
results_s=Compute_Scipy(benchmark_functions)
# print the results
for name, func in benchmark_functions.items():
    print(name," Scipy=",results_s[name]," Genetic=",results_g[name]," Difference=",(results_g[name]-results_s[name]))


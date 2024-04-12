import numpy as np
import matplotlib.pyplot as plt
import functools
def dominates(fitnesses_1,fitnesses_2):
    # fitnesses_1 is a array of objectives of solution 1 [objective1, objective2 ...]
    larger_or_equal = fitnesses_1 >= fitnesses_2
    larger = fitnesses_1 > fitnesses_2
    if np.all(larger_or_equal) and np.any(larger):
        return True
    return False

def obj1(x):
    return 1 - x * x
def obj2(x):
    return 1 - (x-0.5) * (x-0.5)

def calculate_pareto_fronts(fitnesses):
    
    # Calculate dominated set for each individual
 
    domination_sets = []
    domination_counts = []
    #print(len(fitnesses))
    #print(fitnesses,"*")
    for fitnesses_1 in fitnesses:
        current_dimination_set = set()
        domination_counts.append(0)
        #print(domination_counts)
        for i,fitnesses_2 in enumerate(fitnesses):
            if dominates(fitnesses_1,fitnesses_2):
                current_dimination_set.add(i)
                #print("add ",i,fitnesses_1,fitnesses_2)
            elif dominates(fitnesses_2,fitnesses_1):
                domination_counts[-1] += 1
                #print("sub ",i,fitnesses_2,fitnesses_1)
        domination_sets.append(current_dimination_set)
    #print(domination_sets)
    #print(domination_counts)

    domination_counts = np.array(domination_counts)
    fronts = []
    while True:
        current_front = np.where(domination_counts==0)[0]
        #print("*",current_front)
        if len(current_front) == 0:
            #print("Done")
            break
        #print("Front: ",current_front)
        fronts.append(current_front)
        #print(fronts)
        for individual in current_front:
            domination_counts[individual] = -1 # this individual is already accounted for, make it -1 so  ==0 will not find it anymore
            dominated_by_current_set = domination_sets[individual]
            for dominated_by_current in dominated_by_current_set:
                domination_counts[dominated_by_current] -= 1
    #print(fronts)
    return fronts

def calculate_crowding_metrics(fitnesses,fronts):
    
    num_objectives = fitnesses.shape[1]
    num_individuals = fitnesses.shape[0]
    #print(num_individuals,num_objectives)
    # Normalise each objectives, so they are in the range [0,1]
    # This is necessary, so each objective's contribution have the same magnitude to the crowding metric.
    normalized_fitnesses = np.zeros_like(fitnesses)
    #print(normalized_fitnesses)
    for objective_i in range(num_objectives):
        min_val = np.min(fitnesses[:,objective_i])
        max_val = np.max(fitnesses[:,objective_i])
        #print(fitnesses)
        #print(min_val,max_val)
        val_range = max_val - min_val
        normalized_fitnesses[:,objective_i] = (fitnesses[:,objective_i] - min_val) / val_range
        #print("**",normalized_fitnesses)
    
    fitnesses = normalized_fitnesses
    crowding_metrics = np.zeros(num_individuals)

    for front in fronts:
        for objective_i in range(num_objectives):
            #print(front)
            sorted_front = sorted(front,key = lambda x : fitnesses[x,objective_i])
            #print(sorted_front,"|",sorted_front[0],"|",sorted_front[-1])
            crowding_metrics[sorted_front[0]] = np.inf
            crowding_metrics[sorted_front[-1]] = np.inf
            #print(crowding_metrics)
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
# Some generic GA functions
def touranment_selection(num_parents,num_offspring):
    offspring_parents = []
    for _ in range(num_offspring):
        contestants = np.random.randint(0,num_parents,2) # generate 2 random numbers, take the smaller (parent list is already sorted, smaller index, better)
        winner = np.min(contestants)
        offspring_parents.append(winner)
    
    return offspring_parents

# simple mutation
def get_mutated_copy(parent,min_val,max_val,mutation_power_ratio):
    mutation_power = (max_val - min_val) * mutation_power_ratio
    offspring = parent.copy()
    offspring += np.random.normal(0,mutation_power,size = offspring.shape)
    offspring = np.clip(offspring,min_val,max_val)
    return offspring



def NSGA2_create_next_generation(pop,fitnesses,config):
    
    # algorithm and task parameters
    half_pop_size = config["half_pop_size"]
    problem_dim = config["problem_dim"]
    gene_min_val = config["gene_min_val"]
    gene_max_val = config["gene_max_val"]
    mutation_power_ratio = config["mutation_power_ratio"]

    # calculate the pareto fronts and crowding metrics
    
    fronts = calculate_pareto_fronts(fitnesses)
    print(len(fronts))
    nondomination_rank_dict = fronts_to_nondomination_rank(fronts)
    #print(nondomination_rank_dict)
    crowding = calculate_crowding_metrics(fitnesses,fronts)
    #print("//",crowding)
    # Sort the population
    non_domiated_sorted_indicies = nondominated_sort(nondomination_rank_dict,crowding)
    print(non_domiated_sorted_indicies)
    # The better half of the population survives to the next generation and have a chance to reproduce
    # The rest of the population is discarded
    surviving_individuals = pop[non_domiated_sorted_indicies[:half_pop_size]]
    #print((surviving_individuals))
    reproducing_individual_indicies = touranment_selection(num_parents=half_pop_size,num_offspring=half_pop_size)
    print(len(reproducing_individual_indicies))
    #print(pop)
    offsprings = np.array([get_mutated_copy(surviving_individuals[i],gene_min_val,gene_max_val,mutation_power_ratio) for i in reproducing_individual_indicies])
    
    new_pop = np.concatenate([surviving_individuals,offsprings])  # concatenate the 2 lists
    return new_pop
def simple_1d_fitness_func(x):
    objective_1 = 1-(x * x)
    objective_2 = 1-((x-0.5) * (x-0.5))
    return np.stack([objective_1,objective_2],axis=1)

config = {
    "half_pop_size" : 20,
    "problem_dim" : 1,
    "gene_min_val" : -1,
    "gene_max_val" : 1,
    "mutation_power_ratio" : 0.05,
}

pop = np.random.uniform(config["gene_min_val"],config["gene_max_val"],2*config["half_pop_size"])
#print(pop)
mean_fitnesses = []
for generation in range(100):
    
    # evaluate pop
    fitnesses = simple_1d_fitness_func(pop)
    #print(fitnesses)
    mean_fitnesses.append(np.mean(fitnesses,axis=0))
    #print(mean_fitnesses)
    # transition to next generation
    pop = NSGA2_create_next_generation(pop,fitnesses,config)
    
# Check if we found the same solutions as the brute force method
x = np.linspace(-1,1,100)
all_solutions_fitnesses = simple_1d_fitness_func(x)
plt.plot(all_solutions_fitnesses[:,0],all_solutions_fitnesses[:,1])
plt.plot(fitnesses[:config["half_pop_size"],0],fitnesses[:config["half_pop_size"],1],".",color="red")
plt.xlabel("obj1")
plt.ylabel("obj2")
plt.show()

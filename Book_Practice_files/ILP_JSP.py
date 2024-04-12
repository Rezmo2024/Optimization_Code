import pulp
import random
import matplotlib.pyplot as plt
def Draw_Solution(data,makespan):
    fig, ax = plt.subplots()
    machine_colors = {1: 'tab:blue', 2: 'tab:orange', 3: 'tab:green', 4: 'tab:pink',5: 'tab:purple',6: 'tab:cyan'}
    y_ticks = list(set(machine for _, machine in data.keys()))
    # Create bars for each job on different machines
    for  ((job, machine), (start, end)) in data.items():
        ax.broken_barh([(start, end )], (y_ticks.index(job), 1), facecolors=machine_colors[machine], edgecolor='black')
        ax.text(start + (end ) / 2, y_ticks.index(job) + 0.5, f'Job {machine}', ha='center', va='center', color='Black',weight='bold')
    # Set y ticks and labels
    ax.set_yticks(range(len(y_ticks)))
    ax.set_xticks(range(makespan))
    ax.set_yticklabels([f'Machine {machine}' for machine in y_ticks])
    ax.set_xlabel('Time')
    ax.set_title('Gantt Chart Table')
    plt.show()
# Define the parameters
J = range(1, 4)
M =  range(1, 4)
m = len(M)
#p = {(h - 1, j): int(round(random.random()*10)) for h in range(2, m + 2) for j in J}
p={(1, 1): 3, (1, 2): 3, (1, 3): 6, (2, 1): 8, (2, 2): 5, (2, 3): 9, (3, 1): 10, (3, 2): 4, (3, 3): 6}
V = sum(p[(h-1,j)] for h in range(2, m + 2) for j in J)
C = pulp.LpVariable("C", lowBound=0, cat="Continuous")
y = pulp.LpVariable.dicts("y", [(j, k, i) for j in J for k in J for i in M], cat="Binary")
x = pulp.LpVariable.dicts("x", [(i, j) for i in M for j in J], lowBound=0, cat="Continuous")
# Initialize the problem
prob = pulp.LpProblem("ILP Model", pulp.LpMinimize)
# Define the objective function
prob += C
# constraint 1
for h in range(2, m + 1):
    for j in J:
        prob += x[h - 1, j] + p[h - 1, j] <= x[h, j]
# constraint 2,3
for j in J:
    for k in J:
        for i in range(1, m + 1):
            if j != k:
                prob += x[i, k] + p[i, k] - V * y[i, j, k] <= x[i, j]
                prob += x[i, j] + p[i, j] - V * (1 - y[i, j, k]) <= x[i, k]
# constraint 4
for j in J:
        prob += x[m, j] + p[m, j] <= C
# Solve the problem
prob.solve()
print(prob)
# Print the solution
for j in J:
    for k in J:
        for i in M:
            if j != k:
                print(f"y_{j, k, i} = {y[j, k, i].varValue}")
print("Status:", pulp.LpStatus[prob.status])
print("Objective value:", prob.objective.value())
schedule={}
for j in J:
    for i in M:
        print(f"x_{i, j} = {x[i, j].varValue}")
        schedule[(i,j)]=(x[i, j].varValue,p[(i,j)])
print(schedule)
Draw_Solution(schedule,int(prob.objective.value())+1)
from itertools import product
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value,LpStatus
import matplotlib.pyplot as plt
def Draw_Solution(jobs,x_ticks):
    # Create a Gantt chart with job labels
    fig,ax = plt.subplots(figsize=(12, 6))
    for i, (job, (start, end)) in enumerate(jobs.items()):
        if end - start > 0:
            ax.broken_barh([(start, end - start)], (i - 0.4, 0.8), facecolors=(0.9, 0.9, 0.9),edgecolors='black')
            ax.text(start + (end - start) / 2, i, job, ha='center', va='center', color='black', weight='bold')
    # Set labels and title
    ax.set_xticks(range(x_ticks+1))
    ax.set_yticks(range(len(jobs)))
    ax.set_yticklabels([])
    ax.set_xlabel('Time')
    ax.set_title('RCPSP Gantt Chart')
    plt.show()
n = 10  # note there will be exactly 12 jobs (n=10 jobs plus the two 'dummy' ones)
p = [0, 3, 2, 5, 4, 2, 3, 4, 2, 4, 6, 0]
u = [[0, 0], [5, 1], [0, 4], [1, 4], [1, 3], [3, 2], [3, 1], [2, 4],
     [4, 0], [5, 2], [2, 5], [0, 0]]
c = [6, 8]
S = [[0, 1], [0, 2], [0, 3], [1, 4], [1, 5], [2, 9], [2, 10], [3, 8], [4, 6],
     [4, 7], [5, 9], [5, 10], [6, 8], [6, 9], [7, 8], [8, 11], [9, 11], [10, 11]]
(R, J, T) = (range(len(c)), range(len(p)), range(sum(p)))
model = LpProblem("RCPSP", LpMinimize)
x = [[LpVariable('x({},{})'.format(j, t), cat='Binary') for t in T] for j in J]
#objective
model+=lpSum(t * x[n + 1][t] for t in T)
#Constraint 1
for j in J:
    model += lpSum(x[j][t] for t in T) == 1
#Constraint 2
for (r, t) in product(R, T):
    model += (lpSum(u[j][r] * x[j][t2] for j in J for t2 in range(max(0, t - p[j] + 1), t + 1))<= c[r])
#Constraint 3
for (j, s) in S:
    model += lpSum(t * x[s][t] - t * x[j][t] for t in T) >= p[j]

model.solve()
# Print the results
jobs={}
print(model)
print(f'Status: {LpStatus[model.status]}')
print("Schedule: ")
for (j, t) in product(J, T):
    if value(x[j][t]) == 1:
        print("Job {}: begins at t={} and finishes at t={}".format(j, t, t+p[j]))
        index="Job "+str(j)
        jobs[index]=(t,t+p[j])
print("Makespan = {}".format(value(model.objective)))
Draw_Solution(jobs,int(value(model.objective)))
print(jobs)

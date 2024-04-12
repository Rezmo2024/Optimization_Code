from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value,LpStatus
import matplotlib.pyplot as plt
from itertools import product
import numpy as np
#function to draw each cell
def draw_cell(x, y,numbers,N,label,colors):
    r = 1
    angle = np.linspace(0, 2*np.pi, N+1)
    plt.text(x, y+1.2, label, color='black', fontsize=12, ha='center', va='center')
    for i in range(N):
        plt.fill([x, x + r*np.cos(angle[i]), x + r*np.cos(angle[i+1])],
                 [y, y + r*np.sin(angle[i]), y + r*np.sin(angle[i+1])],
                 color=colors[i])
        x_center = x + 0.5 * ((r -0.2) * np.cos(angle[i]) + (r -0.2)* np.cos(angle[i + 1]))
        y_center = y + 0.5 * ((r -0.2) * np.sin(angle[i]) + (r -0.2) * np.sin(angle[i + 1]))       
        plt.text(x_center, y_center, numbers[i], color='black', fontsize=12, ha='center', va='center')
#function to draw solution of the model
def Draw_Solution(N,freq):
    plt.figure(figsize=(8, 4))
    num_sides = 6
    rad=1.09
    colors = plt.cm.tab10(np.linspace(0, 1, N*N)*10)
    for i in range(N):
        angles = np.linspace(0, 2*np.pi, num_sides, endpoint=False)
        if N//2>(i):
            x=i*2.3
            y= 5
        else:
            x=(i-N//2)*2.3 
            y= 2        
        x_coords = x + rad * np.cos(angles)
        y_coords = y + rad * np.sin(angles)
        x_coords = np.append(x_coords, x_coords[0])
        y_coords = np.append(y_coords, y_coords[0])  
        plt.plot(x_coords, y_coords, marker='.',color='black')
        if N//2>(i):
            draw_cell(i*2.3, 5,freq[i],len(freq[i]),'Cell '+str(i),colors)
        else:
            draw_cell((i-N//2)*2.3, 2,freq[i],len(freq[i]),'Cell '+str(i),colors)
    plt.axis('equal')
    plt.axis('off')
    plt.show()        
# number of channels per node
r = [3, 5, 8, 3, 6, 5, 7, 3]
# distance between channels in the same node (i, i) and in adjacent nodes
#      0  1  2  3  4  5  6  7
d = [[3, 2, 0, 0, 2, 2, 0, 0],   # 0
     [2, 3, 2, 0, 0, 2, 2, 0],   # 1
     [0, 2, 3, 0, 0, 0, 3, 0],   # 2
     [0, 0, 0, 3, 2, 0, 0, 2],   # 3
     [2, 0, 0, 2, 3, 2, 0, 0],   # 4
     [2, 2, 0, 0, 2, 3, 2, 0],   # 5
     [0, 2, 2, 0, 0, 2, 3, 0],   # 6
     [0, 0, 0, 2, 0, 0, 0, 3]]   # 7

N = range(len(r))
U = range(sum(d[i][j] for (i, j) in product(N, N)) + sum(el for el in r))
m= LpProblem("BCMP", LpMinimize)
# Define the decision variables
z =  LpVariable(name=f"z", lowBound=0, cat='Continuous') 
x = {}
for c in U:
    for i in N:
            x[i,c] = LpVariable(f'x_{i}_{c}', cat='Binary')
#objective
m+=z
#constarint 1
for i in N:
    m += lpSum(x[i,c] for c in U) == r[i]
#constarint 2
for i, j, c1, c2 in product(N, N, U, U):
    if i != j and c1 <= c2 < c1+d[i][j]:
        m += x[i,c1] + x[j,c2] <= 1
#constarint 3
for i, c1, c2 in product(N, U, U):
    if c1 < c2 < c1+d[i][i]:
        m += x[i,c1] + x[i,c2] <= 1
#constarint 4
for i, c in product(N, U):
    m += z >= (c+1)*x[i,c]
m.solve()
print(m)
# Print the results
print(f"Optimal value of Z : {value(m.objective)}")
print(f'Status: {LpStatus[m.status]}')
freq={}
for i in N:
        freq[i]=[]
        for c in U:
            if value(x[i,c]) >0:
                 freq[i].append(c)
print(freq)
Draw_Solution(len(r),freq)

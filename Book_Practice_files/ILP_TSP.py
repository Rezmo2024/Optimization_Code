from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value,LpStatus
import networkx as nx
import matplotlib.pyplot as plt
def plot_tour(edges,label):
    G = nx.DiGraph()
    for edge in edges:
        start, end = map(int, edge[1:-1].split(','))
        G.add_edge(start, end)
    pos = nx.spring_layout(G)
    fig, ax = plt.subplots(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, ax=ax)
    edge_labels = {(u, v): f"({u},{v})" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    plt.title("Traveling Salesman Tour with Total Cost="+label)
    plt.show()
#10 cities
dist_matrix = [
    [0, 99, 110, 46, 68, 52, 72, 79, 12, 94],
    [99, 0, 400, 46, 97, 31, 77, 12, 92, 48],
    [110, 400, 0, 65, 0, 46, 35, 69, 17, 73],
    [46, 46, 65, 0, 68, 33, 40, 13, 31, 0],
    [68, 97, 0, 68, 0, 40, 70, 73, 31, 19],
    [52, 31, 46, 33, 40, 0, 83, 0, 34, 21],
    [72, 77, 35, 40, 70, 83, 0, 45, 0, 12],
    [79, 12, 69, 13, 73, 0, 45, 0, 31, 92],
    [12, 92, 17, 31, 31, 34, 0, 31, 0, 0],
    [94, 48, 73, 0, 19, 21, 12, 92, 0, 0]
]
n = len(dist_matrix)
V = list(range(n))
# Create the PuLP minimization problem
prob = LpProblem("TSP", LpMinimize)
# Define the decision variables
x = {(i, j): LpVariable(name=f"x_{i}_{j}", cat='Binary') for i in V for j in V if i != j}
y = {i: LpVariable(name=f"y_{i}", lowBound=0, cat='Continuous') for i in V}
# Define the objective function
prob += lpSum(dist_matrix[i][j] * x[i, j] for i in V for j in V if i != j), "Total Cost"
# Add constraints
for i in V:
    prob += lpSum(x[i, j] for j in V if i != j) == 1, f"Out_Constraint_{i}"
    prob += lpSum(x[j, i] for j in V if i != j) == 1, f"In_Constraint_{i}"
for i in V[1:]:
    for j in V[1:]:
        if i != j:
            prob += y[i] - (n + 1) * x[i, j] >= y[j] - n, f"Subtour_Constraint_{i}_{j}"
# Solve the problem
prob.solve()
print(prob)
# Print the results
print(f"Optimal value of Z (Total Cost): {value(prob.objective)}")
print("Optimal Tour:")
print(f'Status: {LpStatus[prob.status]}')
tour = []
for i in V:
    for j in V:
        if i != j and value(x[i, j]) == 1:
            tour.append("("+str(i)+","+str(j)+")")
print(tour)
plot_tour(tour,str({value(prob.objective)}))

import numpy as np
import matplotlib.pyplot as plt
def f(x):
    return -x**4-10*x
def g(x):
    return 4 + x**10+ x**2+x
x = np.linspace(0, 2, 100)
f_values = [f(xi) for xi in x]
g_values = [g(xi) for xi in x]
# Find the Pareto optimal points
pareto_x = []
pareto_f = []
pareto_g = []
for i in range(len(x)):
    is_pareto_optimal = True
    for j in range(len(x)):
        if f_values[j] <= f_values[i] and g_values[j] <= g_values[i] and (f_values[j] < f_values[i] or g_values[j] < g_values[i]):
            is_pareto_optimal = False
            break
    if is_pareto_optimal:
        pareto_x.append(x[i])
        pareto_f.append(f_values[i])
        pareto_g.append(g_values[i])
plt.figure(figsize=(8, 6))
plt.scatter(f_values, g_values, label='All points',color='blue')
plt.scatter(pareto_f, pareto_g, color='black', label='Pareto front')
plt.xlabel('f(x) = -x^4-10x')
plt.ylabel('g(x) = 4 + x^10+ x^2+x')
plt.title('Pareto Front')
plt.legend()
plt.show()        
#Capacitated Facility Location
import pulp
REQUIRE = {
 'A' : 7,
 'B' : 4,
 'C' : 5,
 'D' : 3,
 'E' : 4,
 'F' : 6
 }
WorkStations = ['A','B','C','D','E','F']
SW_LOCATIONS = ['L1','L2','L3','L4']
SW_CAPACITY = 8
prob = pulp.LpProblem("CapacitatedFacilityLocation", pulp.LpMinimize)
use_vars = pulp.LpVariable.dicts("U", SW_LOCATIONS, 0, 1, pulp.LpBinary)
waste_vars = pulp.LpVariable.dicts("W", SW_LOCATIONS, 0, SW_CAPACITY)
assign_vars = pulp.LpVariable.dicts("A",[(i, j) for i in SW_LOCATIONS for j in WorkStations], 0, 1, pulp.LpBinary)
#Objective function
prob += pulp.lpSum(waste_vars[i] for i in SW_LOCATIONS)
#constarints
for j in WorkStations:
 prob += pulp.lpSum(assign_vars[(i, j)] for i in SW_LOCATIONS) == 1
for i in SW_LOCATIONS:
 prob += pulp.lpSum(assign_vars[(i, j)] * REQUIRE[j] for j in WorkStations) + waste_vars[i] == SW_CAPACITY * use_vars[i]

prob.solve()
print(prob)
for i in SW_LOCATIONS:
 if use_vars[i].varValue > 0:
     print("Switch ", i, " Connects ",  [j for j in WorkStations if assign_vars[(i, j)].varValue])
print(f'Status: {pulp.LpStatus[prob.status]}')
print("Optimal solution=",pulp.value(prob.objective))

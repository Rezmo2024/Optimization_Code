import random
import numpy as np

class Person:
    def __init__(self, node_count):
        self.data = np.zeros(node_count)
        self.sol = np.zeros(node_count, dtype=int)
        self.parent = np.zeros(node_count, dtype=int)
        self.cost = np.zeros(node_count)
        self.delay = np.zeros(node_count)
        self.stop = np.zeros(node_count, dtype=int)
    def Get_DataValue(self, index):
        return self.data[index]
    def Set_DataValue(self, index, value):
        self.data[index] = value
    def Get_SolutionValue(self, index):
        return self.sol[index]
    def Set_SolutionValue(self, index, value):
        self.sol[index] = value
    def Get_ParentValue(self, index):
        return self.parent[index]
    def Set_ParentValue(self, index, value):
        self.parent[index] = value
    def Get_CostValue(self, index):
        return self.cost[index]
    def Set_CostValue(self, index, value):
        self.cost[index] = value
    def Get_DelayValue(self, index):
        return self.delay[index]
    def Set_DealyValue(self, index, value):
        self.delay[index] = value
    def Get_StopValue(self, index):
        return self.stop[index]
    def Set_StopValue(self, index, value):
        self.stop[index] = value

class TLBO_CSP:
    def __init__(self, cost, delay, src, dst, dlthresh, iter, pc):
        self.cost = cost
        self.delay = delay
        self.npop = 0
        self.MAXIt = iter
        self.node_count = len(cost)
        self.thrdelay = dlthresh
        self.source = src 
        self.destination = dst
        self.Bestsol = []
        self.Tree = []
        self.Find_Solution = False
        for k in range(self.node_count):
            for j in range(self.node_count):
                if self.cost[k][j] == 0:
                    self.cost[k][j] = float('inf')
        self.npop = int(self.node_count * pc)

    def initialize(self):
        var = 0.0
        visited = [False] * self.node_count
        for k in range(self.node_count):
            visited[k] = False
        for k in range(len(self.destination)):
            newbestsol = Person(self.node_count)
            newbestsol.Set_CostValue(self.destination[k], float('inf'))
            newbestsol.Set_DealyValue(self.destination[k], float('inf'))
            newbestsol.Set_StopValue(self.destination[k], -1)
            self.Bestsol.append(newbestsol)
        # extract edges
        edges=[]
        for p in range(self.node_count):
            for q in range(self.node_count):
                if self.cost[p][q]!=float('inf'):
                        edges.append(self.cost[p][q])
        rand = random.Random()
        for i in range(self.npop):
            newPerson = Person(self.node_count)
            newPerson.Set_DataValue(0, var)
            for j in range(1, self.node_count):
                var= edges[rand.randint(0, len(edges)-1)]
                newPerson.Set_DataValue(j, 1 / var)
            self.persons.append(newPerson)
            self.GetTotalCost(newPerson)
            self.GetTotalDelay(newPerson)
            for k in range(len(self.destination)):
                if newPerson.Get_CostValue(self.destination[k])!=0 and newPerson.Get_DelayValue(self.destination[k])!=0 and newPerson.Get_CostValue(self.destination[k]) < self.Bestsol[k].Get_CostValue(self.destination[k]) and newPerson.Get_DelayValue(self.destination[k]) <= self.thrdelay:
                    self.copyPerson(self.Bestsol[k], newPerson)

    def Teaching_phase(self):
        Teacher = self.persons[0]
        mean = np.zeros(self.node_count)
        for j in range(self.node_count):
            for i in range(self.npop):
                mean[j] += self.persons[i].Get_DataValue(j)
            mean[j] /= self.npop

        for i in range(1, self.npop):
            if self.persons[i].Get_CostValue(self.destination[0]) < Teacher.Get_CostValue(self.destination[0]):
                Teacher = self.persons[i]

        for i in range(self.npop):
            newsol = Person(self.node_count)
            TF = 0
            value = 0.0
            if random.random() < 0.5:
                TF = 1
            else:
                TF = 2
            for j in range(self.node_count):
                rand = random.uniform(0, self.node_count)
                value = self.persons[i].Get_DataValue(j) + rand * (Teacher.Get_DataValue(j) - TF * mean[j])
                newsol.Set_DataValue(j, value)
            self.Make_Solution(newsol)
            self.GetTotalCost(newsol)
            self.GetTotalDelay(newsol)
            flag = True
            for p in range(len(self.destination)):
                if newsol.Get_CostValue(self.destination[p]) >= self.persons[i].Get_CostValue(self.destination[p]) or newsol.Get_DelayValue(self.destination[p]) > self.thrdelay:
                    flag = False
                    break
            if flag:
                self.copyPerson(self.persons[i], newsol)
            for k in range(len(self.destination)):
                if newsol.Get_CostValue(self.destination[k])!=0 and newsol.Get_DelayValue(self.destination[k])!=0 and newsol.Get_CostValue(self.destination[k]) < self.Bestsol[k].Get_CostValue(self.destination[k]) and newsol.Get_DelayValue(self.destination[k]) <= self.thrdelay:
                    self.copyPerson(self.Bestsol[k], newsol)


    def Learning_phase(self):
        rand = random.Random()
        for i in range(self.npop):
            flag = True
            step = np.zeros(self.node_count)
            newsol = Person(self.node_count)
            k = i
            while i == k:
                k = rand.randint(0, self.npop - 1)
            for j in range(self.node_count):
                step[j] = self.persons[i].Get_DataValue(j) - self.persons[k].Get_DataValue(j)
            for p in range(len(self.destination)):
                if self.persons[k].Get_CostValue(self.destination[p]) >= self.persons[i].Get_CostValue(self.destination[p]):
                    flag = False
                    break
            if flag:
                for j in range(self.node_count):
                    rand2 = random.uniform(0, self.node_count)
                    value = self.persons[i].Get_DataValue(j) + rand2 * step[j]
                    newsol.Set_DataValue(j, value)
                self.Make_Solution(newsol)
                self.GetTotalCost(newsol)
                self.GetTotalDelay(newsol)
                flag = True
                for p in range(len(self.destination)):
                    if newsol.Get_CostValue(self.destination[p]) >= self.persons[i].Get_CostValue(self.destination[p]) or newsol.Get_DelayValue(self.destination[p]) > self.thrdelay:
                        flag = False
                        break
                if flag:
                    self.copyPerson(self.persons[i], newsol)
            for p in range(len(self.destination)):
                if  newsol.Get_CostValue(self.destination[p])!=0 and newsol.Get_DelayValue(self.destination[p])!=0 and newsol.Get_CostValue(self.destination[p]) < self.Bestsol[p].Get_CostValue(self.destination[p]) and newsol.Get_DelayValue(self.destination[p]) <= self.thrdelay:
                    self.copyPerson(self.Bestsol[p], newsol)

    def GetTotalCost(self, thisPerson):
        for j in range(len(self.destination)):
            thisPerson.Set_CostValue(self.destination[j], 0.0)
            for i in range(self.node_count):
                if thisPerson.Get_SolutionValue(i) == self.destination[j]:
                    thisPerson.Set_StopValue(self.destination[j], i)
                    break
                elif i < self.node_count - 1:
                    thisPerson.Set_CostValue(self.destination[j], thisPerson.Get_CostValue(self.destination[j]) + self.cost[thisPerson.Get_SolutionValue(i)][thisPerson.Get_SolutionValue(i + 1)])

    def GetTotalDelay(self, thisPerson):
        for j in range(len(self.destination)):
            thisPerson.Set_DealyValue(self.destination[j], 0)
            for i in range(self.node_count):
                if thisPerson.Get_SolutionValue(i) == self.destination[j]:
                    thisPerson.Set_StopValue(self.destination[j], i)
                    break
                elif i < self.node_count - 1:
                    thisPerson.Set_DealyValue(self.destination[j], thisPerson.Get_DelayValue(self.destination[j]) + self.delay[thisPerson.Get_SolutionValue(i)][thisPerson.Get_SolutionValue(i + 1)])

    def Make_Solution(self, a):
        rand = random.Random()
        cnt = -1      
        visited = [False] * self.node_count
        a.Set_SolutionValue(0, self.source)
        for j in range(self.node_count):
            visited[j] = False
        visited[self.source] = True
        for i in range(1, self.node_count):
            sum = 0
            cnt = i
            parent = a.Get_SolutionValue(i - 1)
            done = False
            while not done:
                k = 0
                neighbor = np.zeros(self.node_count, dtype=int)
                newsolvalue = -1
                for l in range(self.node_count):
                    if self.cost[parent][l] != float('inf') and not visited[l] and self.delay[parent][l] <= self.thrdelay:
                        neighbor[k] = l
                        k += 1
                #Rollet Wheel
                if k != 0:
                    for m in range(k):
                        sum += a.Get_DataValue(neighbor[m])
                    r = rand.uniform(0, 1)
                    tot = 0
                    for j in range(k):
                        if sum==0:
                            tot=0
                        else:
                            tot += (a.Get_DataValue(neighbor[j]) / sum)
                        if tot >= r:
                            newsolvalue = neighbor[j]
                            visited[newsolvalue] = True
                            a.Set_SolutionValue(i, newsolvalue)
                            a.Set_ParentValue(i, cnt - 1)
                            done = True
                            break
                else:
                    if cnt > 0:
                        cnt -= 1
                        parent = a.Get_ParentValue(cnt)
                    else:
                        done = True

    def copyPerson(self, a, b):
        for i in range(self.node_count):
            a.Set_DataValue(i, b.Get_DataValue(i))
            a.Set_SolutionValue(i, b.Get_SolutionValue(i))
            a.Set_ParentValue(i, b.Get_ParentValue(i))
        for i in range(len(self.destination)):
            a.Set_CostValue(self.destination[i], b.Get_CostValue(self.destination[i]))
            a.Set_DealyValue(self.destination[i], b.Get_DelayValue(self.destination[i]))
            a.Set_StopValue(self.destination[i], b.Get_StopValue(self.destination[i]))

    def solve(self):
        self.persons = []
        self.initialize()
        for it in range(self.MAXIt):
            self.Teaching_phase()
            self.Learning_phase()
        self.ReturnBestSolution()

    def ReturnBestSolution(self):
        for i in range(len(self.destination)):
            if self.Bestsol[i].Get_StopValue(self.destination[i])>0:
                for j in range(self.Bestsol[i].Get_StopValue(self.destination[i])+1):
                    print(vertices[self.Bestsol[i].sol[j]],end="=>")
                    if vertices[self.Bestsol[i].sol[j]] not in self.Tree:
                        self.Tree.append(vertices[self.Bestsol[i].sol[j]])
                print("     Delay=",self.Bestsol[i].Get_DelayValue(self.destination[i])," Cost=",self.Bestsol[i].Get_CostValue(self.destination[i]))
            else:
                print("Destination ",vertices[self.destination[i]]," Not Satisfied!!!")
        if len(self.Tree) > 0:
            self.Find_Solution = True
        else:
            self.Find_Solution = False                
        return self.Tree


def Convert_Adjacency(graph_dic):
    vertices = list(graph_dic.keys())
    num_vertices = len(vertices)
    # Initialize the adjacency matrix with zeros
    adjacency_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
    # Iterate through each vertex and its neighbors
    for i, vertex in enumerate(vertices):
        for neighbor, weight in graph_dic[vertex].items():
            j = vertices.index(neighbor)
            adjacency_matrix[i][j] = weight
    # Since it's an undirected graph, add edges in the opposite direction
    for i in range(num_vertices):
        for j in range(i, num_vertices):  # Start from j = i to avoid duplicates
            if adjacency_matrix[i][j] != 0 and adjacency_matrix[j][i] == 0:
                adjacency_matrix[j][i] = adjacency_matrix[i][j]
    adj_list=[]
    for row in adjacency_matrix:
        adj_list.append(row)
    return adj_list

cost = {
  'A': {'B': 4, 'C': 11, 'D': 10},
  'B': {'C': 20, 'E': 1, 'A': 4},
  'C': {'D': 3, 'F': 15, 'A': 11, 'B': 20},
  'D': {'G': 7, 'A': 10, 'C': 3},
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
cost_mat=Convert_Adjacency(cost)
delay_mat=Convert_Adjacency(delay)
vertices = list(cost.keys())
source='A'
destinations=['E','G','F']
s=vertices.index(source)
dests=[]
for i in destinations:
    dests.append(vertices.index(i))
Tlbo_obj=TLBO_CSP(cost_mat,delay_mat,s,dests,20,200,0.6)
Tlbo_obj.solve()
if Tlbo_obj.Find_Solution==True:
    print("Multicast Tree=",Tlbo_obj.Tree)
else:
    print("There is no solution that satisfies the Delay threshold")
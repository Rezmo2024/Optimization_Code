import random

class Ant:
    ALPHA = 1
    BETA = 1
    Q = 1
    Rho = 0.05
    INFINITY = 9999999999.999999
    ITERATION = 1000
    INITIAL_PHEROMONES = 0.0012
    DELAY_THRESH = 0
    
    def __init__(self, mat, iter_, ant_count, del_, dt):
        self.Ants_number = ant_count
        self.ITERATION = iter_
        self.best_cost = self.INFINITY
        self.DELAY_THRESH = dt
        self.Cost_Matrix = self.init_Cost_Matrix(mat)
        self.Delay_Matrix = self.init_delay_matrix(del_)
        self.invertedMatrix = self.invert_matrix()
        self.pheromones = self.initialize_pheromones()
        self.ant_matrix =  self.init_ants(ant_count)
        self.best_path = []
        self.findpath=False
      
    def init_Cost_Matrix(self, m):
        Cost_Matrix = []
        for i in range(len(m)):
            Cost_Matrix.append([])
            for j in range(len(m[i])):
                if m[i][j] != 0:
                    Cost_Matrix[i].append(m[i][j])
                else:
                    Cost_Matrix[i].append(self.INFINITY)
        return Cost_Matrix
    
    def init_delay_matrix(self, m):
        Delay_Matrix = []
        for i in range(len(m)):
            Delay_Matrix.append([])
            for j in range(len(m[i])):
                if m[i][j] != 0:
                    Delay_Matrix[i].append(m[i][j])
                else:
                    Delay_Matrix[i].append(0)
        return Delay_Matrix
    
    def invert_matrix(self):
        invertedMatrix = []
        for i in range(len(self.Cost_Matrix)):
            invertedMatrix.append([])
            for j in range(len(self.Cost_Matrix)):
                invertedMatrix[i].append(1 / self.Cost_Matrix[i][j])
        return invertedMatrix
    
    def initialize_pheromones(self):
        pheromones = [[self.INITIAL_PHEROMONES for _ in range(len(self.Cost_Matrix))] 
                      for _ in range(len(self.Cost_Matrix))]
        return pheromones
    
    def init_ants(self, numAnts):
        ant_matrix =  []
        temp = [-1 for _ in range(len(self.Cost_Matrix))]
        for _ in range(numAnts):
            ant_matrix.append({'path': temp, 'cost': self.INFINITY})
        return ant_matrix
    
    def evaporate(self, last_index_):
        for ant in self.ant_matrix:
            if ant['path'][last_index_] == self.Dest:
                for i in range(last_index_):
                    p = ant['path'][i]
                    q = ant['path'][i+1]
                    self.invertedMatrix[p][q] *= (1 - self.Rho)
    
    def update_pheromone(self, last_index_):
        for ant in self.ant_matrix:
            if ant['path'][last_index_] == self.Dest:
                for i in range(last_index_):
                    p = ant['path'][i]
                    q = ant['path'][i+1]
                    self.invertedMatrix[p][q] += self.Q / ant['cost']
    
    def get_cost(self, p, l_index):
        cost = 0.0
        for i in range(l_index):
            cost += self.Cost_Matrix[p[i]][p[i+1]]
        return cost
    
    def start(self, src, dst):
        self.Src = src
        self.Dest = dst 
        last_index_ = 0
        for _ in range(self.ITERATION):
            for ant in self.ant_matrix:
                ant['path'][0] = self.Src
                last_index_ = 0
                findpath_flag=True
                while ant['path'][last_index_] != self.Dest:
                    q = ant['path'][last_index_]
                    index = self.rollet_wheel(q)
                    if index > 0 and not self.exist(ant['path'], last_index_, index):
                        last_index_ += 1
                        ant['path'][last_index_] = index
                    else:
                        findpath_flag=False
                        break
                if findpath_flag==True and self.satisfy_delay(ant['path'], last_index_):
                    ant['cost'] = self.get_cost(ant['path'], last_index_)
                    self.update_pheromone(last_index_)
                    self.evaporate(last_index_)
                    if ant['cost'] <= self.best_cost or self.get_delay(ant['path'], last_index_) <= self.DELAY_THRESH:
                        self.best_cost = ant['cost']
                        self.DELAY_THRESH = self.get_delay(ant['path'], last_index_)
                        self.best_path = ant['path'][:last_index_+1]
                        self.l_index = last_index_
                        self.findpath = True
    
    def satisfy_delay(self, a, l_index):
        total_delay = self.get_delay(a, l_index)
        return total_delay <= self.DELAY_THRESH
    
    def get_delay(self, a, l_index):
        total_delay = 0
        for i in range(l_index):
            total_delay += self.Delay_Matrix[a[i]][a[i+1]]
        return total_delay

    def exist(self, a, l_index, f):
        return f in a[:l_index+1]
    
    def rollet_wheel(self, rowindex):
        Sum_Prob = sum((self.invertedMatrix[rowindex][x]**self.BETA * self.pheromones[rowindex][x]**self.ALPHA) 
                      for x in range(len(self.Cost_Matrix)) if self.Cost_Matrix[rowindex][x] != self.INFINITY)
        s = random.random()
        sum_ = 0.0
        for x in range(len(self.Cost_Matrix)):
            if self.Cost_Matrix[rowindex][x] != self.INFINITY:
                p = self.invertedMatrix[rowindex][x]**self.BETA * self.pheromones[rowindex][x]**self.ALPHA
            else:
                p = 0
            sum_ += p / Sum_Prob
            if sum_ > s:
                return x
        return -1
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
destination='H'
s=vertices.index(source)
d=vertices.index(destination)
ant_obj=Ant(cost_mat,100,10,delay_mat,20)
ant_obj.start(s,d)
if ant_obj.findpath:
    print(ant_obj.best_path," cost=",ant_obj.get_cost(ant_obj.best_path,len(ant_obj.best_path)-1)," delay=",ant_obj.get_delay(ant_obj.best_path,len(ant_obj.best_path)-1))
    for i in ant_obj.best_path:
        print(vertices[i],end="->")
else:
    print("There is no path taht satisfies the Delay threshold")



from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value,LpStatus
import matplotlib.pyplot as plt
def plot_queen(board):
    n = len(board)
    plt.figure(figsize=(4, 4))
    plt.imshow(board,cmap='copper_r')
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                plt.text(j, i, 'Q', color='White', fontsize=13, ha='center', va='center')
            else:
                plt.text(j, i, 'N', color='Black', fontsize=12, ha='center', va='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()
n=8
queens =LpProblem("N-Queens", LpMaximize)
x = [[LpVariable('x({},{})'.format(i, j), cat='Binary')
      for i in range(n)] for j in range(n)]
#objective
queens += lpSum(x[i][j] for i in range(n) for j in range(n)) 
# one per row
for i in range(n):
    queens += lpSum(x[i][j] for j in range(n)) == 1, 'row({})'.format(i)
# one per column
for j in range(n):
    queens += lpSum(x[i][j] for i in range(n)) == 1, 'col({})'.format(j)
# diagonal \
for p, k in enumerate(range(2 - n, n - 2 + 1)):
    queens += lpSum(x[i][i - k] for i in range(n)if 0 <= i - k < n) <= 1, 'diag1({})'.format(p)
# diagonal /
for p, k in enumerate(range(3, n + n)):
    queens += lpSum(x[i][k - i] for i in range(n)if 0 <= k - i < n) <= 1, 'diag2({})'.format(p)
queens.solve()
print(queens)
board = [[0 for i in range(n)] for j in range(n)]
# Print the results
print(f'Status: {LpStatus[queens.status]}')
#print("Optimal solution=",value(queens.objective))
for i in range(n):
    for j in range(n):
        print(f"{int(value(x[i][j]))}|",end="")
        board[i][j]=int(value(x[i][j]))
    print("\n")
plot_queen(board)

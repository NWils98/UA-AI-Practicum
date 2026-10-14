from ortools.sat.python import cp_model

# Creates the model.
model = cp_model.CpModel()

N=4

board=[]
for i in range(N):
    row=[]
    for j in range(N):
        row.append(model.NewBoolVar("X["+str(i)+"]["+str(j)+"]"))
    board.append(row)

for i in range(N):
    for j in range(N):
        for k in range(i + 1, N):
            model.add(board[i][j] + board[k][j] < 2)

            if j - (k - i) >= 0:
                model.add(board[i][j] + board[k][j - (k - i)] < 2)

            if j + (k - i) < N:
                model.add(board[i][j] + board[k][j + (k - i)] < 2)

        for k in range(j+1,N):
            model.add(board[i][j] + board[i][k]<2)


    model.add(sum(board[i])==1)

solver = cp_model.CpSolver()
status = solver.Solve(model)


# Statistics.
print('\nStatistics')
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())

if status != cp_model.INFEASIBLE:
    for i in range(N):
        for j in range(N):
            if solver.Value(board[i][j]):
                print("Q",end="")
            else:
                print(".",end="")
        print()
else:
        print('Geen oplossing')
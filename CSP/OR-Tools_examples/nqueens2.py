from ortools.sat.python import cp_model

# Creates the model.
model = cp_model.CpModel()

N=4

queens=[model.NewIntVar(1,N,"Q"+str(i)) for i in range(N)]
model.AddAllDifferent(*queens)

for i in range(N):
    for j in range(i+1,N):
        model.Add(queens[i] - queens[j] != j - i)
        model.Add(queens[j] - queens[i] != j - i)

solver = cp_model.CpSolver()
status = solver.Solve(model)


# Statistics.
print('\nStatistics')
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())

if status != cp_model.INFEASIBLE:
    for i in range(N):
        print(solver.Value(queens[i]))
else:
    print("No solution")
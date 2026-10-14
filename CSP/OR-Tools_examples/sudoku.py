from ortools.sat.python import cp_model

# Creates the model.
model = cp_model.CpModel()

# Data.
rijen=[[] for _ in range(9)]
kolommen=[[] for _ in range(9)]
blokken=[[] for _ in range(9)]
for i in range(9):
    for j in range(9):
        vak = model.NewIntVar(1, 9, "C["+str(i)+"]["+str(j)+"]")
        rijen[i].append(vak)
        kolommen[j].append(vak)
        blokken[(i//3)*3+(j//3)].append(vak)

for i in range(9):
    model.AddAllDifferent(*rijen[i])
    model.AddAllDifferent(*kolommen[i])
    model.AddAllDifferent(*blokken[i])

model.Add(rijen[1][1]==2)
model.Add(rijen[1][7]==8)
model.Add(rijen[6][3]==5)

solver = cp_model.CpSolver()
status = solver.Solve(model)

# Statistics.
print('\nStatistics')
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())

if status != cp_model.INFEASIBLE:
    print(solver.Value(rijen[8][6]),solver.Value(rijen[8][7]))
else:
    print('Geen oplossing')
from ortools.sat.python import cp_model

# Creates the model.
model = cp_model.CpModel()
T=model.NewIntVar(1,9,"T")
W=model.NewIntVar(0,9,"W")
O=model.NewIntVar(0,9,"O")
F=model.NewIntVar(1,9,"F")
U=model.NewIntVar(0,9,"U")
R=model.NewIntVar(0,9,"R")
C1=model.NewIntVar(0,9,"C1")
C2=model.NewIntVar(0,9,"C2")

model.add(2*O==R+10*C1)
model.add(2*W+C1==U+10*C2)
model.add(2*T+C2==F*10+O)
model.AddAllDifferent(T,W,O,F,U,R)

solver = cp_model.CpSolver()
status = solver.Solve(model)


# Statistics.
print('\nStatistics')
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())

if status != cp_model.INFEASIBLE:
    for L in [T,W,O,F,U,R]:
        print(L.Name(),"=",solver.Value(L))

else:
    print('Geen oplossing')


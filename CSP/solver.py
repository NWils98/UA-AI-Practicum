from ortools.sat.python import cp_model


def solve_kakuro(row_sums, column_sums, givens):
    # Geef een lijst van lijsten met cijfers terug.
    model = cp_model.CpModel()
    board = None #TODO
    # TODO: Implementeer

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return [[solver.Value(cell) for cell in row] for row in board]
    if status == cp_model.INFEASIBLE:
        return None
    raise RuntimeError('OR-Tools kon geen oplossing of onmogelijkheid vaststellen.')


if __name__ == '__main__':
    row_sums = [3, 7]
    column_sums = [4, 6]
    givens = [(0,0,1)]

    solution = solve_kakuro(row_sums, column_sums, givens)
    print(solution)

"""Check a completed CSV against its puzzle, without consulting an answer file."""
import argparse
from csv_io import load_puzzle, load_solution


def check_grid(puzzle, grid):
    n = puzzle.size
    if not isinstance(grid, (list, tuple)) or len(grid) != n:
        return [f'Geef een lijst met precies {n} rijen terug.']
    if any(not isinstance(row, (list, tuple)) or len(row) != n for row in grid):
        return [f'Elke rij moet precies {n} cijfers bevatten.']
    errors = []
    for r in range(n):
        for c in range(n):
            if type(grid[r][c]) is not int or not 1 <= grid[r][c] <= 9:
                errors.append(f'Vakje ({r+1}, {c+1}): verwacht een geheel cijfer 1-9, kreeg {grid[r][c]!r}.')
    if errors:
        return errors
    for r, c, value in puzzle.givens:
        if grid[r][c] != value:
            errors.append(f'Vakje ({r+1}, {c+1}): het startcijfer {value} is gewijzigd.')
    for r, total in enumerate(puzzle.row_sums):
        if len(set(grid[r])) != n:
            errors.append(f'Rij {r+1}: een cijfer wordt herhaald.')
        if sum(grid[r]) != total:
            errors.append(f'Rij {r+1}: som {sum(grid[r])}, verwacht {total}.')
    for c, total in enumerate(puzzle.column_sums):
        column = [grid[r][c] for r in range(n)]
        if len(set(column)) != n:
            errors.append(f'Kolom {c+1}: een cijfer wordt herhaald.')
        if sum(column) != total:
            errors.append(f'Kolom {c+1}: som {sum(column)}, verwacht {total}.')
    return errors


def main():
    parser = argparse.ArgumentParser(description='Controleer een ingevulde Kakuro-CSV.')
    parser.add_argument('puzzle', help='Originele puzzel-CSV')
    parser.add_argument('solution', help='Ingevulde CSV met dezelfde somaanwijzingen')
    args = parser.parse_args()
    try:
        puzzle = load_puzzle(args.puzzle)
        grid = load_solution(args.solution, puzzle)
        errors = check_grid(puzzle, grid)
    except (OSError, ValueError) as error:
        print(f'FOUT: {error}')
        return 2
    if errors:
        print('NIET CORRECT:')
        for error in errors:
            print(f'  - {error}')
        return 1
    print('CORRECT: alle sommen, unieke cijfers en startcijfers kloppen.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

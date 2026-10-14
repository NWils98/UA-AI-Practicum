"""CSV input/output helpers. You do not need to change this file."""
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Puzzle:
    row_sums: list
    column_sums: list
    givens: list

    @property
    def size(self):
        return len(self.row_sums)


def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        rows = [[cell.strip() for cell in row] for row in csv.reader(handle) if row]
    if not rows or len(rows) < 3 or len(rows) > 10:
        raise ValueError('Een CSV moet 2 tot 9 speelrijen plus een bovenste rij met sommen hebben.')
    n = len(rows)-1
    if any(len(row) != n+1 for row in rows):
        raise ValueError(f'Elke CSV-rij moet {n+1} velden bevatten, gescheiden door komma\'s.')
    if rows[0][0] != '#':
        raise ValueError('Het veld linksboven moet # zijn.')
    return rows


def number(value, label):
    if not value.isascii() or not value.isdigit():
        raise ValueError(f'{label}: verwacht een geheel getal, kreeg {value!r}.')
    return int(value)


def load_puzzle(path):
    data = read_csv(path)
    n = len(data)-1
    rows = [number(data[r+1][0], f'Som rij {r+1}') for r in range(n)]
    columns = [number(data[0][c+1], f'Som kolom {c+1}') for c in range(n)]
    minimum, maximum = n*(n+1)//2, n*(19-n)//2
    if any(not minimum <= total <= maximum for total in rows+columns):
        raise ValueError(f'Een som van {n} verschillende cijfers 1-9 moet tussen {minimum} en {maximum} liggen.')
    if sum(rows) != sum(columns):
        raise ValueError('De som van de rijsommen moet gelijk zijn aan de som van de kolomsommen.')
    givens = []
    for r in range(n):
        for c in range(n):
            value = data[r+1][c+1]
            if value == '?':
                continue
            digit = number(value, f'Vakje ({r+1}, {c+1})')
            if not 1 <= digit <= 9:
                raise ValueError(f'Vakje ({r+1}, {c+1}): een startcijfer moet tussen 1 en 9 liggen.')
            givens.append((r, c, digit))
    return Puzzle(rows, columns, givens)


def load_solution(path, puzzle):
    data = read_csv(path)
    n = puzzle.size
    if len(data) != n+1:
        raise ValueError(f'De oplossing moet {n} speelrijen hebben.')
    rows = [number(data[r+1][0], f'Som rij {r+1}') for r in range(n)]
    columns = [number(data[0][c+1], f'Som kolom {c+1}') for c in range(n)]
    if rows != puzzle.row_sums or columns != puzzle.column_sums:
        raise ValueError('De somaanwijzingen zijn gewijzigd of deze CSV hoort bij een andere puzzel.')
    return [[number(data[r+1][c+1], f'Vakje ({r+1}, {c+1})') for c in range(n)] for r in range(n)]


def write_solution(path, puzzle, grid):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle, lineterminator='\n')
        writer.writerow(['#', *puzzle.column_sums])
        for total, row in zip(puzzle.row_sums, grid):
            writer.writerow([total, *row])

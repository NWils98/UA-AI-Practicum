"""Read a puzzle, call the function, and automatically check the result."""
import argparse
from pathlib import Path
from checker import check_grid
from csv_io import load_puzzle, write_solution


def main():
    parser = argparse.ArgumentParser(description='Voer jouw Kakuro-solver uit en controleer de oplossing.')
    parser.add_argument('puzzle', nargs='?', default=str(Path(__file__).with_name('examples') / '2x2_01.csv'))
    parser.add_argument('--output', help='Bestand voor jouw ingevulde CSV')
    args = parser.parse_args()
    try:
        from solver import solve_kakuro
    except ModuleNotFoundError as error:
        if error.name and error.name.startswith('ortools'):
            print('Installeer OR-Tools eerst: python -m pip install -r requirements.txt')
            return 2
        raise
    try:
        puzzle = load_puzzle(args.puzzle)
        grid = solve_kakuro(puzzle.row_sums, puzzle.column_sums, puzzle.givens)
        if grid is None:
            print('Jouw solver rapporteert geen oplossing. De meegeleverde puzzels zijn wel oplosbaar.')
            return 1
        errors = check_grid(puzzle, grid)
        if errors:
            print('NIET CORRECT:')
            for error in errors:
                print(f'  - {error}')
            return 1
        puzzle_path = Path(args.puzzle)
        default_name = f'{puzzle_path.parent.name}_{puzzle_path.name}'
        output = Path(args.output) if args.output else Path(__file__).with_name('answers') / default_name
        write_solution(output, puzzle, grid)
        print(f'CORRECT. Ingevulde CSV opgeslagen in {output.resolve()}')
        return 0
    except (OSError, ValueError, NotImplementedError, RuntimeError) as error:
        print(f'FOUT: {error}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

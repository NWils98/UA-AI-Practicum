"""Check values against independent, exact retrograde calculations."""
from fractions import Fraction
import argparse
from algorithms import evaluate, StError, NAMES
from game import reachable_boards, utility, legal_moves, play_move, next_player


def reference_tables():
    boards = sorted(reachable_boards(), key=lambda b: b.count('.'))
    minimax, expectimax = {}, {}
    for board in boards:
        score = utility(board)
        if score is not None:
            minimax[board] = score
            expectimax[board] = Fraction(score)
            continue
        player = next_player(board)
        children = [play_move(board, move, player) for move in legal_moves(board)]
        min_values = [minimax[child] for child in children]
        exp_values = [expectimax[child] for child in children]
        minimax[board] = max(min_values) if player == 'X' else min(min_values)
        expectimax[board] = max(exp_values) if player == 'X' else sum(exp_values)/len(exp_values)
    return minimax, expectimax


def default_cases(boards):
    selected = [tuple(text) for text in (
        '.........', 'XX.OO....', 'XX.OO...X', 'XXXOO....', 'XX.OOOX..',
        'XOXXOOOXX', 'XOXOX.O..', 'XO.X.OX.O', 'XX.OO.XOX')]
    # Include a mix of X and O turns, late positions and chance nodes.
    for player in ('X', 'O'):
        candidates = sorted(b for b in boards if next_player(b) == player
                            and utility(b) is None and b.count('.') in (2, 3, 4))
        selected.extend(candidates[::max(1, len(candidates)//5)][:5])
    return list(dict.fromkeys(board for board in selected if board in boards))


def full_search_counts(boards):
    """Exact tree size for exhaustive minimax, with no pruning or caching."""
    counts = {}
    for board in sorted(boards, key=lambda b: b.count('.')):
        children = [play_move(board, move, next_player(board)) for move in legal_moves(board)]
        counts[board] = 1+sum(counts[child] for child in children)
    return counts


def check_search_cases(cases, reference, name, teacher=False):
    failures, generated = 0, 0
    observed_expansion = False
    for board in cases:
        actual, positions = evaluate(board, name, teacher)
        generated += positions
        if utility(board) is None and positions > 1:
            observed_expansion = True
        expected = float(reference[board])
        if abs(actual-expected) > 1e-9:
            failures += 1
            print(f'FOUT {"".join(board)} ({next_player(board)}): kreeg {actual}, verwacht {expected:.10g}.')
    return failures, generated, observed_expansion


def pruning_reduced_work(generated, full_minimax, observed_expansion):
    return observed_expansion and generated < full_minimax


def main():
    parser = argparse.ArgumentParser(description='Controleer de waarde die jouw zoekalgoritme teruggeeft.')
    parser.add_argument('algorithm', choices=NAMES)
    parser.add_argument('--model', action='store_true', help='Controleer de aparte docentuitwerking.')
    parser.add_argument('--all', action='store_true', help='Controleer alle bereikbare speltoestanden.')
    args = parser.parse_args()
    minimax, expectimax = reference_tables()
    reference = expectimax if args.algorithm == 'expectimax' else minimax
    cases = sorted(reference) if args.all else default_cases(reference)
    try:
        failures, generated, observed_expansion = check_search_cases(
            cases, reference, args.algorithm, args.model)
    except StError as error:
        print(f'FOUT: {error}')
        return 2
    if failures:
        print(f'{failures} van {len(cases)} toestanden niet correct.')
        return 1
    if args.algorithm == 'alphabeta':
        full_counts = full_search_counts(reference)
        full_minimax = sum(full_counts[board] for board in cases)
        print(f'Gegenereerde posities (inclusief beginborden): {generated}; volledige minimax: {full_minimax}.')
        if not observed_expansion:
            print('NIET GECONTROLEERD: geen opvolgers gemeten. Gebruik de meegeleverde play_move om opvolgers te maken.')
            return 2
        if not pruning_reduced_work(generated, full_minimax, observed_expansion):
            print('NIET CORRECT: de waarden kloppen, maar de zoekopdracht is niet kleiner dan volledige minimax.')
            return 1
        print(f'CORRECT: {len(cases)} waarden kloppen en de zoekopdracht is kleiner dan volledige minimax.')
    else:
        print(f'CORRECT: {len(cases)} waarden gecontroleerd voor {args.algorithm}; {generated} gegenereerde posities inclusief beginborden.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

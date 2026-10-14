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


def main():
    parser = argparse.ArgumentParser(description='Controleer de waarde die jouw zoekalgoritme teruggeeft.')
    parser.add_argument('algorithm', choices=NAMES)
    parser.add_argument('--model', action='store_true', help='Controleer de aparte docentuitwerking.')
    parser.add_argument('--all', action='store_true', help='Controleer alle bereikbare speltoestanden.')
    args = parser.parse_args()
    minimax, expectimax = reference_tables()
    reference = expectimax if args.algorithm == 'expectimax' else minimax
    cases = sorted(reference) if args.all else default_cases(reference)
    failures = 0
    for board in cases:
        try:
            actual, _ = evaluate(board, args.algorithm, args.model)
        except StError as error:
            print(f'FOUT: {error}')
            return 2
        expected = float(reference[board])
        if abs(actual-expected) > 1e-9:
            failures += 1
            print(f'FOUT {"".join(board)} ({next_player(board)}): kreeg {actual}, verwacht {expected:.10g}.')
    if failures:
        print(f'{failures} van {len(cases)} toestanden niet correct.')
        return 1
    print(f'CORRECT: {len(cases)} toestanden gecontroleerd voor {args.algorithm}.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""Connect the small algorithm files to the provided app and checker."""
from pathlib import Path
import math
import types
from game import legal_moves, next_player, play_move, utility

NAMES = ('minimax', 'alphabeta', 'expectimax')


class StError(ValueError):
    pass


def load_algorithm(name, teacher=False):
    if name not in NAMES:
        raise StError('Onbekend algoritme.')
    folder = Path(__file__).parent
    prefix = ''
    if teacher:
        folder = folder.parent/'tictactoe_docent'
        prefix = 'model'
    path = folder/f'{prefix}{name}.py'
    if not path.is_file():
        raise StError(f'{path.name} is niet gevonden.')
    # Read source on every request, so saved  edits take effect immediately.
    module = types.ModuleType(f'ttt_{prefix}{name}')
    module.__file__ = str(path)
    try:
        exec(compile(path.read_text(encoding='utf-8'), str(path), 'exec'), module.__dict__)
        original = getattr(module, name)
    except Exception as error:
        raise StError(f'{path.name}: {type(error).__name__}: {error}') from error
    calls = [0]
    def counted(*args, **kwargs):
        calls[0] += 1
        return original(*args, **kwargs)
    # Recursive calls in the function are counted too.
    module.__dict__[name] = counted
    return counted, calls


def checked_value(function, board, player, name):
    try:
        value = function(tuple(board), player)
    except Exception as error:
        raise StError(f'{name}: {type(error).__name__}: {error}') from error
    if value is None:
        raise StError(f'Vul {name}.py in. De functie geeft nog None terug.')
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise StError('Geef een eindscore of verwachte score als getal terug.')
    if not -1.000000001 <= value <= 1.000000001:
        raise StError('De score voor X moet tussen -1 en +1 liggen.')
    return value


def evaluate(board, name, teacher=False):
    function, calls = load_algorithm(name, teacher)
    value = checked_value(function, board, next_player(board), name)
    return value, calls[0]


def choose_x_move(board, name, teacher=False):
    if utility(board) is not None or next_player(board) != 'X':
        raise StError('X kan nu geen zet doen.')
    function, calls = load_algorithm(name, teacher)
    best_move, best_value = None, float('-inf')
    for move in legal_moves(board):
        child = play_move(board, move, 'X')
        value = checked_value(function, child, 'O', name)
        if value > best_value:
            best_move, best_value = move, value
    return best_move, best_value, calls[0]

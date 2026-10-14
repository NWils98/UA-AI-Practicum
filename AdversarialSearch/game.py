"""Provided game rules. Empty squares are '.', and positions are numbered 0-8."""
WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None


def utility(board):
    """Return +1 for X, -1 for O, 0 for a draw, or None if play continues."""
    result = winner(board)
    if result == 'X':
        return 1
    if result == 'O':
        return -1
    if '.' not in board:
        return 0
    return None


def legal_moves(board):
    if utility(board) is not None:
        return []
    return [i for i, cell in enumerate(board) if cell == '.']


def other_player(player):
    return 'O' if player == 'X' else 'X'


def next_player(board):
    return 'X' if board.count('X') == board.count('O') else 'O'


def play_move(board, move, player):
    """Return a new board; the original board is unchanged."""
    if player not in ('X', 'O') or player != next_player(board):
        raise ValueError('De verkeerde speler is aan zet.')
    if type(move) is not int or move not in legal_moves(board):
        raise ValueError('Deze zet is niet toegestaan.')
    result = list(board)
    result[move] = player
    return tuple(result)


def reachable_boards():
    """All reachable positions; never continue after a win or draw."""
    initial = ('.',)*9
    seen, pending = {initial}, [initial]
    while pending:
        board = pending.pop()
        for move in legal_moves(board):
            child = play_move(board, move, next_player(board))
            if child not in seen:
                seen.add(child)
                pending.append(child)
    return seen

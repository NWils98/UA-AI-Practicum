from game import utility, legal_moves, play_move, other_player


def expectimax(board, player):
    # TODO: geef de eindscore terug als het spel afgelopen is.
    # TODO: X kiest het maximum van de kindwaarden.
    # TODO: O kiest elke toegestane zet met dezelfde kans: neem het gemiddelde.
    return None


if __name__ == '__main__':
    board = ('X', 'X', '.', 'O', 'O', '.', '.', '.', '.')
    value = expectimax(board, 'X')

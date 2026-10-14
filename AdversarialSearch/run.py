"""Start the visual game. Only Python's standard library is required."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import random
import webbrowser
from algorithms import choose_x_move, StError
from game import reachable_boards, next_player, legal_moves, play_move, utility

ROOT = Path(__file__).resolve().parent
REACHABLE = reachable_boards()


class Handler(BaseHTTPRequestHandler):
    teacher = False

    def send_json(self, data, status=200):
        encoded = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == '/api/info':
            self.send_json({'teacher': self.teacher})
            return
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        content = (ROOT/'index.html').read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path != '/api/move':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 4096:
                raise StError('Ongeldig verzoek.')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict) or not isinstance(data.get('board'), list):
                raise StError('Geef een bord met negen vakjes.')
            raw_board = data['board']
            if len(raw_board) != 9 or any(cell not in ('.', 'X', 'O') for cell in raw_board):
                raise StError('Een bord bevat negen vakjes met X, O of een punt.')
            board = tuple(raw_board)
            if board not in REACHABLE or utility(board) is not None:
                raise StError('Dit bord is geen speelbare toestand.')
            name = data.get('algorithm')
            if next_player(board) == 'O':
                if name != 'expectimax':
                    raise StError('Speel de zet van O zelf op het bord.')
                move = random.choice(legal_moves(board))
                value, nodes = None, 0
                actor = 'O'
            else:
                move, value, nodes = choose_x_move(board, name, self.teacher)
                actor = 'X'
            self.send_json({'board': list(play_move(board, move, actor)), 'move': move,
                            'player': actor, 'value': value, 'nodes': nodes})
        except (StError, ValueError, TypeError, KeyError) as error:
            self.send_json({'error': str(error)}, 400)

    def log_message(self, *_args):
        pass


def main():
    parser = argparse.ArgumentParser(description='Start boter-kaas-en-eieren.')
    parser.add_argument('--port', type=int, default=8001)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--model', action='store_true', help='Gebruik de aparte oplossingsmodel.')
    args = parser.parse_args()
    Handler.teacher = args.model
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError as error:
        parser.exit(1, f'Kon de app niet starten: {error}\nProbeer --port 0.\n')
    url = f'http://127.0.0.1:{server.server_port}/'
    print(f'{url}  (Ctrl+C om te stoppen)', flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()

"""Run the Kakuro browser app using only Python's standard library."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import webbrowser

APP_FILE = Path(__file__).resolve().with_name('index.html')


class KakuroHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.partition('?')[0]
        if path not in ('/', '/index.html'):
            self.send_error(404)
            return
        document = APP_FILE.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(document)))
        self.end_headers()
        self.wfile.write(document)

    def log_message(self, *_args):
        pass


def main():
    parser = argparse.ArgumentParser(description='Open the Kakuro puzzle in your browser.')
    parser.add_argument('--port', type=int, default=8000,
                        help='Local port (default: 8000; use 0 for an available port).')
    parser.add_argument('--no-browser', action='store_true',
                        help='Print the address without opening a browser.')
    args = parser.parse_args()
    if not APP_FILE.is_file():
        parser.error('Keep run.py and index.html in the same folder.')
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), KakuroHandler)
    except OSError as error:
        parser.exit(1, f'Could not start the app: {error}\nTry running with --port 0.\n')
    url = f'http://127.0.0.1:{server.server_port}/'
    print(f'Kakuro is running at {url}', flush=True)
    print('Keep this terminal open. Press Ctrl+C to stop.', flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nKakuro stopped.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()

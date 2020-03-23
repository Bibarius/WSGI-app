import sys
import os
import mimetypes
from wsgiref import simple_server, util
from urllib.parse import urlparse, parse_qs


class Form():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ['REQUEST_METHOD'] == 'POST':
            print(environ['CONTENT_TYPE'])
            print('length = ', environ['CONTENT_LENGTH'])
            length = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(length)
            parsed = parse_qs(data)
            email = str(parsed[b'email'][0], 'utf-8')
            password = str(parsed[b'password'][0], 'utf-8')
            print(email, ' ', password)
            # print('email = ', parsed[b'email'])
        return self.app(environ, start_response)


def frontend(environ, respond):

    fn = os.path.join(path, environ['PATH_INFO'][1:])
    if '.' not in fn.split(os.path.sep)[-1]:
        fn = os.path.join(fn, 'index.html')
    type = mimetypes.guess_type(fn)[0]

    if os.path.exists(fn):
        respond('200 OK', [('Content-Type', type)])
        return util.FileWrapper(open(fn, "rb"))
    else:
        respond('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'not found']

frontend = Form(frontend)

if __name__ == '__main__':
    path = 'frontend/'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    httpd = simple_server.make_server('', port, frontend)
    print("Serving {} on port {}, control-C to stop".format(path, port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.")
        httpd.server_close()
import sys
import os
import time
import mimetypes
from wsgiref import simple_server, util
from urllib.parse import urlparse, parse_qs
from auth import Auth
from http.cookies import SimpleCookie


class Form():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/':
            length = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(length)
            parsed = parse_qs(data)
            email = str(parsed[b'email'][0], 'utf-8')
            password = str(parsed[b'password'][0], 'utf-8')
            
            with open("database/users.txt", 'a') as file_handler:
                file_handler.write(email)
                file_handler.write(',')
                file_handler.write(password)
                file_handler.write('\n')

        elif environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/login.html':
            length = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(length)
            parsed = parse_qs(data)
            email = str(parsed[b'email'][0], 'utf-8')
            password = str(parsed[b'password'][0], 'utf-8')

            with open("database/users.txt", 'r') as file_handler:
                for user in file_handler:
                    if user == '\n':
                        continue
                    db_email, db_password = user.split(',')
                    db_password = db_password[:-1]
                    if email == db_email and password == db_password:
                        session_id = time.time()
                        
                        environ['session_id'] = session_id

                        with open("database/sessions.txt", 'a') as sessions:
                            sessions.write(str(session_id))
                            sessions.write(str('\n'))

                        environ['wsgi_authorised'] = True


        return self.app(environ, start_response)


def frontend(environ, respond):
    
    fn = os.path.join(path, environ['PATH_INFO'][1:])

    if environ['wsgi_authorised'] == True:  #?поверка авторизации
        fn = 'frontend/success.html'

    elif '.' not in fn.split(os.path.sep)[-1]:
        fn = os.path.join(fn, 'index.html')
 
    type = mimetypes.guess_type(fn)[0]

    if os.path.exists(fn) and 'session_id' in environ:
        respond('200 OK', [('Content-Type', type), ("set-cookie", "session_id" + "=" + str(environ['session_id']))])
        return util.FileWrapper(open(fn, "rb"))
    elif os.path.exists(fn):
        respond('200 OK', [('Content-Type', type)])
        return util.FileWrapper(open(fn, "rb"))
    else:
        respond('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'not found']

frontend = Form(frontend)
frontend = Auth(frontend)


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
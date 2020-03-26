from urllib.parse import urlparse, parse_qs
import database.database as db
import uuid

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
            
            db.add_user(email, password)

        elif environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/login.html':
            length = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(length)
            parsed = parse_qs(data)
            email = str(parsed[b'email'][0], 'utf-8')
            password = str(parsed[b'password'][0], 'utf-8')

            if db.find_user(email, password):
                session_id = int(uuid.uuid1().fields[0])
                environ['session_id'] = session_id

                db.add_session(email, password, session_id)
                environ['wsgi_authorised'] = True

        return self.app(environ, start_response)

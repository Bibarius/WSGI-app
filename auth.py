from http.cookies import SimpleCookie
from paste.session import SessionMiddleware
from urllib.parse import urlparse, parse_qs
import time

class Auth():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        if 'HTTP_COOKIE' in environ:
            cookie = SimpleCookie(environ['HTTP_COOKIE'])
            sessions = []
            with open("database/sessions.txt") as file_handler:
                for line in file_handler:
                    sessions.append(line[:-1])

            if 'session_id' in cookie and cookie['session_id'].coded_value in sessions:
                environ['wsgi_authorised'] = True
 
            else:
                environ['wsgi_authorised'] = False

        else:
            environ['wsgi_authorised'] = False


        return self.app(environ, start_response)
        


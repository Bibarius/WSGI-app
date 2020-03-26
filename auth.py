from http.cookies import SimpleCookie
from paste.session import SessionMiddleware
from urllib.parse import urlparse, parse_qs
import time
import database.database as db

class Auth():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        if 'HTTP_COOKIE' in environ:
            cookie = SimpleCookie(environ['HTTP_COOKIE'])

            if environ['PATH_INFO'] == '/logout.html':
                db.delete_session(cookie['session_id'].coded_value)
                environ['wsgi_authorised'] = False
                environ['PATH_INFO'] = '/login.html'
                return self.app(environ, start_response)


            if 'session_id' in cookie and db.find_session(cookie['session_id'].coded_value):
                environ['wsgi_authorised'] = True
 
            else:
                environ['wsgi_authorised'] = False

        else:
            environ['wsgi_authorised'] = False


        return self.app(environ, start_response)
        


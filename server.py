import sys
import os
import uuid
import mimetypes
from wsgiref import simple_server, util
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader
from auth import Auth
from form import Form
from http.cookies import SimpleCookie
import database.database as db


@Auth
@Form
def frontend(environ, respond):

    if 'css' in environ['PATH_INFO']:
        type = 'text/css'
        fn = os.path.join('templates/', environ['PATH_INFO'][1:])
        respond('200 OK', [('Content-Type', type)])
        return util.FileWrapper(open(fn, "rb"))

    env = Environment(loader=FileSystemLoader('templates/'))
    if environ['PATH_INFO'] == '/': 
        page_name = 'authorized.html' if environ['wsgi_authorised'] else 'register.html'

    if environ['PATH_INFO'] == '/login.html':
        page_name = 'authorized.html' if environ['wsgi_authorised'] else 'login.html'

    type = 'text/html'
    template = env.get_template(page_name)
    response = bytes(template.render(), 'utf-8')
    if 'session_id' in environ:
        respond('200 OK', [('Content-Type', type), ("set-cookie", "session_id" + "=" + str(environ['session_id']))])
    else:
        respond('200 OK', [('Content-Type', type)])
    return [response]



if __name__ == '__main__':
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    httpd = simple_server.make_server('', port, frontend)
    print("Serving on port {}, control-C to stop".format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.")
        httpd.server_close()
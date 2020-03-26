import sys
import os
import uuid
import mimetypes
from wsgiref import simple_server, util
from urllib.parse import urlparse, parse_qs
from auth import Auth
from form import Form
from http.cookies import SimpleCookie
import database.database as db


@Auth
@Form
def frontend(environ, respond):
    
    fn = os.path.join(path, environ['PATH_INFO'][1:])

    if environ['wsgi_authorised'] == True:  #?поверка авторизации
        if '.' not in fn.split(os.path.sep)[-1] or fn == 'frontend/login.html':
            fn = 'frontend/dashboard.html'

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
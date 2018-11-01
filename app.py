import os
import sys
import tornado.gen as gen
import tornado.ioloop as ioloop
import tornado.web as web
import tornado.httpserver as httpserver

from db import load_db
from settings import load_settings


class MainHandler(web.RequestHandler):
    # https://www.tornadoweb.org/en/stable/gen.html
    @gen.coroutine
    def get(self):
        db = self.settings['db']
        collection = db.test_collection
        result = yield collection.insert_one({'key': 'value'})
        print('result %s' % repr(result.inserted_id))
        print(dir(result))
        print(result.inserted_id)
        self.write("Hello World")


def make_app(app_settings):
    return web.Application([
        (r"/", MainHandler),
    ], **app_settings)


if __name__ == '__main__':
    env = 'dev' if len(sys.argv) < 2 else sys.argv[1]
    if env not in ('dev', 'prod'):
        sys.exit(1)
    load_settings(env)
    db_settings = {
        'port': int(os.getenv('DB_PORT')),
        'host': os.getenv('DB_HOST'),
        'name': os.getenv('DB_NAME')
    }
    app_settings = {
        'autoreload': bool(os.getenv('AUTORELOAD')),
        'debug': bool(os.getenv('DEBUG')),
        'serve_traceback': bool(os.getenv('SERVE_TRACEBACK')),
        'db': load_db(db_settings)
    }
    print(app_settings)
    app = make_app(app_settings)
    port = int(os.getenv('SERVE_PORT'))
    if env == 'dev':
        app.listen(port)
    elif env == 'prod':
        server = httpserver.HTTPServer(app)
        server.bind(port)
        server.start(0)  # forks one process per cpu
    ioloop.IOLoop.current().start()

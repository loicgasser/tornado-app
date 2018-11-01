import os
import sys
from tornado import web, ioloop, httpserver

from settings import load_settings, get_app_settings
from urls import url_patterns


def make_app(app_settings):
    return web.Application(url_patterns, **app_settings)


if __name__ == '__main__':
    env = 'dev' if len(sys.argv) < 2 else sys.argv[1]
    if env not in ('dev', 'prod'):
        sys.exit(1)
    load_settings(env)
    app_settings = get_app_settings()
    app = make_app(app_settings)
    print(app_settings)
    port = int(os.getenv('SERVE_PORT'))
    if env == 'dev' or env == 'prod':
        app.listen(port)
    # TODO
    # https://github.com/tornadoweb/tornado/issues/2426#issuecomment-400895086
    # we should use another process manager before going to prod
    elif env == 'prod':
        server = httpserver.HTTPServer(app)
        server.bind(port)
        server.start(0)  # forks one process per cpu
    ioloop.IOLoop.current().start()

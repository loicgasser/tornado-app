import app
from settings import load_settings, get_app_settings
from tornado.testing import AsyncTestCase, gen_test


class TestDraftHandler(AsyncTestCase):

    # override get_app to return a tornado application
    def get_app(self):
        load_settings('dev')
        return app.make_app(get_app_settings())

    def test_dummy(self):
        self.assertEqual('dummy', 'dummy')
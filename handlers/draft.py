from tornado import gen, ioloop, web, httpserver, escape
from bson.objectid import ObjectId


class DBMixin:

    def initialize(self):
        self.db = self.settings['db']
        self.collection = self.db.test_collection


class DraftHandlerGet(DBMixin, web.RequestHandler):

    SUPPORTED_METHODS = ('GET')  # 405 not allowed if something else

    # https://www.tornadoweb.org/en/stable/gen.html
    @gen.coroutine
    def get(self, _id):
        try:
            result = yield self.collection.find_one({'_id': ObjectId(_id)})
            response = {
                '_id': str(result['_id'])
            }
            self.set_status(200)
            self.write(response)
        except Exception as e:
            print('Failed to get a collection')
            self.set_status(400)
            response = {
                'error': e.args[0]
            }
            self.write(response)


class DraftHandlerPost(DBMixin, web.RequestHandler):

    SUPPORTED_METHODS = ('POST')  # 405 not allowed if something else

    def initialize(self):
        self.db = self.settings['db']
        self.collection = self.db.test_collection

    @gen.coroutine
    def post(self):
        request_data = escape.json_decode(self.request.body)
        if ('deck' not in request_data.keys() or 'sideboard' not in request_data.keys()) or \
                (request_data['deck'] is None or request_data['sideboard'] is None):
            self.set_status(400)
            response = {
                'error': 'missing part deck or sideboard'
            }
            return
        try:
            result = yield self.collection.insert_one(request_data)
            response = {
                '_id': str(result.inserted_id)
            }
            self.set_status(200)
            self.write(response)
        except Exception as e:
            print('Failed to insert a new collection')
            self.set_status(400)
            response = {
                'error': e.args[0]
            }
            self.write(response)
        self.finish()
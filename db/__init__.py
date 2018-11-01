from motor import motor_tornado


def load_db(db_settings):
    client = motor_tornado.MotorClient(
        'mongodb://{}:{}'.format(db_settings['host'], db_settings['port']))
    return client[db_settings['name']]

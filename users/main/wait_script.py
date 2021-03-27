from time import sleep

from dj_database_url import config
from psycopg2 import OperationalError, connect


DATABASE_CONFIG = config('DATABASE_URL', engine=False, default='postgres://postgres:1@127.0.0.1:5432/users')
DATABASE = DATABASE_CONFIG['NAME']
USER = DATABASE_CONFIG['USER']
PASSWORD = DATABASE_CONFIG['PASSWORD']
PORT = DATABASE_CONFIG['PORT']
HOST = DATABASE_CONFIG['HOST']


while True:
    try:
        connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
    except OperationalError:
        print('Waiting...! Could not connect to database.')
        sleep(0.2)
    else:
        break

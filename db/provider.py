import psycopg2
from misc.singleton import Singleton


class DBProvider(metaclass=Singleton):
    def __init__(self, db_url):
        print('connection opened')
        self.connect = psycopg2.connect(db_url, sslmode='require')
        self.connect.set_session(autocommit=True)

    def __del__(self):
        print('connection closed')
        self.connect.close()

    def execute(self, cmd):
        with self.connect.cursor() as cursor:
            cursor.execute(cmd)

    def fetchone(self, cmd):
        with self.connect.cursor() as cursor:
            cursor.execute(cmd)
            res = cursor.fetchone()
        return res

    def fetchall(self, cmd):
        with self.connect.cursor() as cursor:
            cursor.execute(cmd)
            res = cursor.fetchall()
        return res

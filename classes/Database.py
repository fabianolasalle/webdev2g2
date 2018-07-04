import pymysql

class Database:
    conn = None

    @staticmethod
    def getConn():
        if Database.conn is None:
            Database.conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='webdev2g2t1')
        return Database.conn

    @staticmethod
    def closeConn():
        if Database.conn is not None:
            Database.conn.close()
            Database.conn = None
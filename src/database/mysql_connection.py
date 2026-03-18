import pymysql

def get_mysql_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='tinyurl',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
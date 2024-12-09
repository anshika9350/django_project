import mysql.connector

class DB_Connection:
    DATABASE_HOST = '192.168.1.23'
    DATABASE_USER = 'khushal'
    DATABASE_PASSWORD = '1234'
    DATABASE_NAME = 'khatabook'
    DATABASE_PORT = 3306

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=self.DATABASE_HOST,
            user=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            database=self.DATABASE_NAME,
            port=self.DATABASE_PORT
        )

    def execute_query(self, query):
        cursor = self.mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_non_query(self, query):
        cursor = self.mydb.cursor()
        cursor.execute(query)
        self.mydb.commit()
        cursor.close()
        return 'success'


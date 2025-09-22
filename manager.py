import sqlite3
import mysql.connector


class Connection():
    def __init__(self):
        self.myresult = []
        try:
            db = self.connection(['host', 'name', 'password'])
            cursor = db.cursor()
            cursor.execute(self.sql())
            self.myresult = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")

    def connection(self, db_connection: list):
        """ user wait host, user, password"""
        if len(db_connection) != 3:
            raise Exception("db_connection isn't all arguments for connection!")
        mydb = mysql.connector.connect(
            host=db_connection[0],
            user=db_connection[1],
            password=db_connection[2]
        )
        return mydb

    def sql(self):
        return "SELECT * FROM customers WHERE address LIKE '%way%'"


conn = Connection()
for row in conn.myresult:
    print(row)
from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error

class DB_Manager():
    def __init__(self):
        pass

    class Connection():
        def connection(self, db_connection: list):
            if len(db_connection) != 3:
                raise Exception("db_connection isn't all arguments for connection!")
            self.db = mysql.connector.connect(
                host=db_connection[0],
                user=db_connection[1],
                password=db_connection[2],
                database="mydatabase"
            )
            return self.db

conn = DB_Manager.Connection()
conn.connection(['localhost', 'root', '*********'])



class Manager():
    def __init__(self, connection):
        self.connection = connection
    
    @contextmanager
    def get_cursor(self):
        db_connection = self.connection.cursor(dictionary=True)
        try:
            yield db_connection
        finally:
            db_connection.close()

    def get(self, table: str, columns: tuple[str], where=None, params=()):
        if not table.isidentifier():
            raise ValueError(f"Invalid table name: {table}")
        for col in columns:
            if not col.isidentifier():
                raise ValueError(f"Invalid column name: {col}")
    
        cols = ', '.join(columns)
        sql = f"SELECT {cols} FROM `{table}`"
        if where:
            sql += f" WHERE {where}"

        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def create_table(self, table: str, fields: tuple[tuple[str, str], ...] | None = None):
        if not table.isidentifier():
            raise ValueError(f"Invalid table name: {table}")
        
        if not fields:
            raise ValueError("No fields specified")

        if not all(isinstance(f, tuple) and len(f)==2 for f in fields):
            raise ValueError("Fields must be tuple(name, type)") 

        drop_command = f"DROP TABLE IF EXISTS `{table}`"
        cols_sql = ', '.join(f"`{name}` {dtype}" for name, dtype in fields)
        create_sql = f'CREATE TABLE {table} ({cols_sql})'
        try:
            with self.get_cursor() as cursor:
                cursor.execute(drop_command)
                cursor.execute(create_sql)
            self.connection.commit()
            print(f"{table}: created successfully!")
        except Error as er:
            print(f"Error working with MySQL: {er}")


manager = Manager(conn.db)
rows = manager.get(table='users', columns=('PersonID',))


table = manager.create_table("users", (("PersonID", "int"),))
for i in rows:
    print(i)
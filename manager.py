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
conn.connection(['localhost', 'root', '85200258'])



class Model():
    __tablename__: str = None
    __fields__: dict = None

    def __init__(self, db):
        self.db = db

    @contextmanager
    def get_cursor(self):
        db_connection = self.db.cursor(dictionary=True)
        try:
            yield db_connection
        finally:
            db_connection.close()

    def get_values(self, columns: tuple[str], where=None, params=()):
        if not self.__tablename__.isidentifier():
            raise ValueError(f"Invalid table name: {self.__tablename__}")

        for col in columns:
            if not col.isidentifier():
                raise ValueError(f"Invalid column name: {col}")
    
        cols = ', '.join(columns)
        sql = f"SELECT {cols} FROM `{self.__tablename__}`"
        if where:
            sql += f" WHERE {where}"

        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def create_table(self):
        if not self.__tablename__.isidentifier():
            raise ValueError(f"Invalid table name: {self.__tablename__}")
        
        if not self.__fields__:
            raise ValueError("No fields specified")

        drop_command = f"DROP TABLE IF EXISTS `{self.__tablename__}`"

        # `id` VARCHAR
        cols_sql = ', '.join(f"`{name_col}` {self.__fields__[name_col].sql_formate()}" for name_col in self.__fields__.keys())
        create_sql = f'CREATE TABLE {self.__tablename__} ({cols_sql})'
        try:
            with self.get_cursor() as cursor:
                cursor.execute(drop_command)
                cursor.execute(create_sql)
            self.db.commit()
            print(f"{self.__tablename__}: created successfully!")
        except Error as er:
            print(f"Error working with MySQL: {er}")
    

    class CharField:
        def __init__(self, max_len:int=None, null:bool=True):
            self.max_len=max_len
            self.null=null
        
        def sql_formate(self):
            return f'VARCHAR {self.max_len}'
        

class UserModel(Model):
    __tablename__ = "users"
    __fields__ = {
        'id': Model.CharField(max_len=250),
        'name': Model.CharField(max_len=200),
    }

userModel = UserModel(conn.db)
userModel.create_table( (("PersonID", "int"),))



    # fields = {
    #     'id': Column(Itnteger),

    # }
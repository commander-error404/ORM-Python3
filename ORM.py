from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error
from settings import DB_HOST
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
conn.connection(DB_HOST)



class Model():
    __tablename__: str = None
    __fields__: dict = None

    def __init__(self, db):
        self.db = db

    @staticmethod
    def disable_foreign_key_checks(db):
        """Disables foreign key checking""" 
        with db.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        db.commit()
#region OFF
    @staticmethod
    def enable_foreign_key_checks(db):

        """Enables foreign key checking""" 
        with db.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        db.commit()
#region ON
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
        
    def add_values(self, columns: tuple[str], values: tuple):
        if not self.__tablename__.isidentifier():
            raise ValueError(f"Invalid table name: {self.__tablename__}")
        
        for col in columns:
            if not col.isidentifier():
                raise ValueError(f"Invalid column name: {col}")

        cols = ', '.join(columns)
        print("*****************simple join ", cols)
        placeholders = ', '.join(['%s'] * len(values))
        print("*****************advenced ", placeholders)
        sql = f'INSERT INTO {self.__tablename__} ({cols}) VALUES ({placeholders})'

        with self.get_cursor() as cursor:
            cursor.execute(sql, values)
            self.db.commit()
            return 'ok'

    def create_table(self):
        if not self.__tablename__.isidentifier():
            raise ValueError(f"Invalid table name: {self.__tablename__}")
        
        for col_name in self.__fields__.keys():
            if not col_name.isidentifier():
                raise ValueError('Invalide column name')
        
        if not self.__fields__:
            raise ValueError("No fields specified")

        # `personId` INT
        cols_sql = ', '.join(f"`{name_col}` {self.__fields__[name_col].sql_format(name_col)}" for name_col in self.__fields__.keys())
        create_sql = f'CREATE TABLE IF NOT EXISTS `{self.__tablename__}` ({cols_sql})'
        print(create_sql)
        try:
            with self.get_cursor() as cursor:
                cursor.execute(create_sql)
            self.db.commit()
            print(f"{self.__tablename__}: created successfully!")
        except Error as er:
            print(f"Error working with MySQL: {er}")
    
    # def delete_table(self):
    #     if not self.__tablename__.isidentifier():
    #         raise ValueError(f"Invalid table name: {self.__tablename__}")

    def delete_values(self, id: int):
        if not self.__tablename__.isidentifier():
            raise ValueError(f"Invalid table name: {self.__tablename__}")
        sql = f'DELETE FROM {self.__tablename__} WHERE id = %s'

        with self.get_cursor() as cursor:
            cursor.execute(sql, (id,))
            self.db.commit()
            return 'ok'

    def update_value(self, id, colums: tuple, params: tuple,):
        if not self.__tablename__.isidentifier():
            raise ValueError(f"Invalid table name: {self.__tablename__}")

        cols = ' = %s'.join(colums) + '= %s'
        sql =  f"UPDATE {self.__tablename__} SET {cols}  WHERE id = %s"

        with self.get_cursor() as cursor:
            cursor.execute(sql, (*params, id))
            self.db.commit()
            return 'ok'


    class CharField:
        def __init__(
            self,
            max_length: int=250,
            null: bool=False, 
            unique: bool=False,
            primary_key: bool=False,
            help_text: str=''
        ):
            self.max_length=max_length
            self.null=null
            self.unique=unique
            self.primary_key=primary_key
            self.help_text=help_text

        def sql_format(self, name_col: str):
            null_str='' if self.null else 'NOT NULL'
            unique_str='UNIQUE'if self.unique== True else''
            pk_str='PRIMARY KEY' if self.primary_key == True else''

            sql = ' '.join(filter(None, [null_str, unique_str, pk_str]))
            print(f'[+]Column --[{name_col}] {sql}')
            return f'VARCHAR({self.max_length}) {sql}'.strip()


    class IntegerField:
        def __init__(
            self,
            null: bool=False, 
            unique: bool=False,
            primary_key: bool=False,
            auto_increment: bool=False,
            help_text: str=''
        ):
            self.null=null
            self.unique=unique
            self.primary_key=primary_key
            self.help_text=help_text
            self.auto_increment = auto_increment


        def sql_format(self, name_col: str):
            null_str='' if self.null else 'NOT NULL'
            unique_str='UNIQUE'if self.unique== True else''
            pk_str='PRIMARY KEY' if self.primary_key == True else''
            auto_increment = 'AUTO_INCREMENT' if self.auto_increment else ''

            sql = ' '.join(filter(None, [auto_increment, null_str, unique_str, pk_str]))
            print(f'[+]Column --[{name_col}] INT {sql}')
            return f'INT {sql}'.strip()


    class BooleanField:
        def __init__(
            self,
            null: bool = False, 
            unique: bool = False,
            default: bool = False,
            help_text: str = ''
        ):
            self.null = null
            self.unique = unique
            self.default = default
            self.help_text = help_text

        def sql_format(self, name_col: str):
            null_str='' if self.null else 'NOT NULL'
            unique_str='UNIQUE'if self.unique== True else''
            default_str = f'DEFAULT {1 if self.default else 0}'
            sql = ' '.join(filter(None, [null_str, unique_str, default_str]))
            return f'TINYINT(1) {sql}'.strip()


    class ImageField():
        def __init__(
                self, 
                upload_to: str = '/', 
                blank: bool = True, 
                unique: bool=True, 
                max_size: int = 50
        ):
            self.upload_to=upload_to
            self.blank=blank
            self.unique=unique
            self.max_size=max_size


        def sql_format(self, name_col: str):
            null_str='' if self.blank else 'NOT NULL'
            unique_str='UNIQUE'if self.unique== True else''

            sql = ' '.join(filter(None, [null_str, unique_str]))
            print(f'[+]Column --[{name_col}] {sql}')
            return f'VARCHAR(250) {sql}'.strip()


    class ForeignKey:
        def __init__(self, model, CASCADE=False, reference:str='id'):
            self.model=model
            self.CASCADE=CASCADE
            self.reference=reference

        def sql_format(self, name_col: str):
            cascade_sql = 'ON DELETE CASCADE' if self.CASCADE else 'ON DELETE RESTRICT'
            
            ref = self.reference  # id
            model = self.model  # UserModel
            field = model.__fields__[self.reference]
            print("+++++++++", field)
            
            TYPE='INT' if isinstance(field, Model.IntegerField) else 'VARCHAR(11)'

            return (
                f'{TYPE}, FOREIGN KEY (`{name_col}`) '
                f'REFERENCES `{self.model.__tablename__}` (`{self.reference}`) {cascade_sql}'
            )


class UserModel(Model):
   __tablename__ = 'cat'
   __fields__ = {
        'id': Model.IntegerField(primary_key=True, auto_increment=True, unique=True),
        'first_name':Model.CharField(max_length=150, help_text='User name'),
        'last_name':Model.CharField(max_length=150, help_text='User name'),
    }


class Car(Model):
    __tablename__ = "Car"

    __fields__ = {
        'car_brand':Model.CharField(max_length=30),
        'car_type': Model.CharField(max_length=30),
        'owner': Model.ForeignKey(UserModel, CASCADE=True, reference="id"),
        'image': Model.ImageField(upload_to='/data', blank=True, unique=False,)
    }


Model.disable_foreign_key_checks(conn.db)

model = UserModel(conn.db)
# model.create_table()
# model.add_values(
#     columns=('name',),
#     values=('Doe',)
# )
# a = model.get_values(('id', 'name','profile'))
# print(a)
# model = Car(conn.db)
# model.create_table()
print(model.update_value(27, ('category',), ('test',)))
Model.enable_foreign_key_checks(conn.db)
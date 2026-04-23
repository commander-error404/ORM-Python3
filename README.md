# 🐍 ORM-Python3

> ⚠️ **WARNING: This project is still under active development. This is NOT a final version. Use it with caution — bugs and breaking API changes are possible.**

A simple ORM (Object-Relational Mapping) system for MySQL/MariaDB, written in Python 3. This project was created **purely for learning purposes** — to understand how ORM works under the hood: how Python objects map to SQL tables, how queries are built, and how relationships between tables are managed.


## 📌 About

This project is a **learning experiment**, not a production-ready library. The goal is to understand how popular ORMs (like Django ORM or SQLAlchemy) work at a low level by implementing the core mechanics from scratch:

- Defining table schemas using Python classes
- Automatic SQL query generation (`CREATE TABLE`, `INSERT`, `SELECT`, `DELETE`)
- Support for basic field types
- Foreign keys (`FOREIGN KEY`) with cascade delete
- Context manager for cursor management

---

## ⚙️ Requirements

- Python 3.10+
- MySQL or MariaDB server
- Dependencies from `requirement.txt`:

```
mysql-connector-python
```

---

## 📦 Installation

```bash
git clone https://github.com/commander-error404/ORM-Python3.git
cd ORM-Python3
pip install -r requirement.txt
```

---

## 🔧 Configuration

Open `settings.py` and set your database connection details:

```python
DB_HOST = ["localhost", "your_user", "your_password"]
```

> The default database name is `mydatabase`. Change it inside the `Connection` class in `ORM.py` if needed.

---

## 🚀 Usage

### Defining a Model

```python
from ORM import Model

class UserModel(Model):
    __tablename__ = 'users'
    __fields__ = {
        'id': Model.IntegerField(primary_key=True, auto_increment=True, unique=True),
        'first_name': Model.CharField(max_length=150),
        'last_name': Model.CharField(max_length=150),
    }
```

### Creating a Table

```python
from ORM import conn

model = UserModel(conn.db)
model.create_table()
```

### Inserting Data

```python
model.add_values(
    columns=('first_name', 'last_name'),
    values=('John', 'Doe')
)
```

### Fetching Data

```python
rows = model.get_values(columns=('id', 'first_name', 'last_name'))
print(rows)
```

### Deleting a Record by ID

```python
model.delete_values(id=1)
```

### Foreign Key

```python
class Car(Model):
    __tablename__ = 'cars'
    __fields__ = {
        'car_brand': Model.CharField(max_length=30),
        'owner': Model.ForeignKey(UserModel, CASCADE=True, reference='id'),
    }
```

---

## 🧩 Available Fields

| Field           | Description                                         | SQL Type             |
|-----------------|-----------------------------------------------------|----------------------|
| `CharField`     | String with a max length constraint                 | `VARCHAR(n)`         |
| `IntegerField`  | Integer, supports `AUTO_INCREMENT`                  | `INT`                |
| `BooleanField`  | Boolean value                                       | `TINYINT(1)`         |
| `DateTimeField` | Date and time, supports `auto_now` / `auto_now_add` | `DATETIME`           |
| `ImageField`    | Path to an image file                               | `VARCHAR(250)`       |
| `ForeignKey`    | Relationship to another model                       | `INT` + `FOREIGN KEY`|

---

## 📋 Model Methods

| Method                        | Description                              |
|-------------------------------|------------------------------------------|
| `create_table()`              | Creates the table in the database        |
| `add_values(columns, values)` | Inserts a new record                     |
| `get_values(columns, where)`  | Returns a list of records                |
| `delete_values(id)`           | Deletes a record by `id`                 |
| `disable_foreign_key_checks`  | Disables foreign key constraint checks   |
| `enable_foreign_key_checks`   | Enables foreign key constraint checks    |

---

## 🚧 Development Status

```
⚠️  THIS IS NOT A FINAL VERSION  ⚠️
```

This project is **still in development** and was built solely for learning. Please keep the following in mind before using it:

- ❌ **Do not use in production** — the code has not been fully tested
- ⚡ **API may change** — class and method interfaces will be revised over time
- 🐛 **Bugs may exist** — the project is at an early stage; known issues are being fixed
- 🔒 **Security** — full protection against SQL injection is not guaranteed in the current version

If you'd like to help or share your knowledge — **contributions and feedback are very welcome!**

---

## 👤 Author

**Redmi** ([@commander-error404](https://github.com/commander-error404))

> This project was created to understand how ORM works at a low level. If you have experience or knowledge in this area — I'd love to collaborate!

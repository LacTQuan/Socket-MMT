import sqlite3

# Create a file (if not exist) and connect to it
conn = sqlite3.connect("employee.db")  # Or ":memory:" for in-memory database -> reset everytime we run => Can be use for testing
# Create a cursor to execute sql command
c = conn.cursor()


# # CREATE A TABLE (it will create an error if we try to run the command twice)
# # Datatypes in SQLite: https://www.sqlite.org/datatype3.html
# c.execute("CREATE TABLE users (username text, psw text)")

# # ADD VALUE
# c.execute("INSERT INTO users VALUES ('Tan', '123')")
# conn.commit()

# #  SELECT ROW
# c.execute("SELECT * FROM users WHERE psw='456'")

# # GET SELECTED ROW
# print(c.fetchone())
# c.fetchmany(<size>)
# print(c.fetchall())

# user_1 = ('DangDecTen', '456')
# user_2 = ('MinhMinh', '456')
# user_3 = ('LacTQuan', '456')
# c.execute("INSERT INTO users VALUES (?, ?)", user_1)
# c.execute("INSERT INTO users VALUES (?, ?)", user_2)
# c.execute("INSERT INTO users VALUES (?, ?)", user_3)
# conn.commit()
# c.execute("SELECT * FROM users WHERE psw=?", ('123',))
# print(c.fetchall())

# NOTE: Remember to commit your changes if you feel it is needed
conn.commit()

conn.close()

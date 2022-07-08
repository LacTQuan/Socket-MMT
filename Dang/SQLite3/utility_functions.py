import sqlite3

conn = sqlite3.connect("employee.db")
c = conn.cursor()

# "employee.db" already exist with values
# -> No need to CREATE A TABLE


def insert_user(user):
    with conn:  # No need to commit changes
        c.execute("INSERT INTO users VALUES (?, ?)", user)


def get_user_by_name(name):
    c.execute("SELECT * FROM users WHERE username=?", (name,))
    return c.fetchall()


def update_password(user, newPsw):
    with conn:
        c.execute("UPDATE users SET psw=? WHERE username=?", (newPsw, user[0]))


def remove_user(user):
    with conn:
        c.execute("DELETE from users WHERE username=? AND psw=?", user)


# Testing
user_1 = ('Anonymous', '789')
user_2 = ('Gladious', '789')

c.execute("SELECT * FROM users WHERE username='Anonymous'")
if c.fetchone():
    print("Found!")
else:
    print("Not found...")

conn.close()

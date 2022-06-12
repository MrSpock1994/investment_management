import sqlite3

# Creating the User DataBase
conn = sqlite3.connect("user_database.db")
# creating a cursor
cursor = conn.cursor()
# create table
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    name text,
    username text,
    email text,
    password text)
    """)

conn.commit()
conn.close()
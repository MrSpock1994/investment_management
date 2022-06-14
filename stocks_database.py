import sqlite3

# Creating the User DataBase
conn = sqlite3.connect("stock_database.db")
# creating a cursor
cursor = conn.cursor()
# create table
cursor.execute("""CREATE TABLE IF NOT EXISTS stocks (
    name text,
    amount float,
    unit_price float)
    """)

conn.commit()
conn.close()
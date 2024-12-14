import sqlite3

conn = sqlite3.connect("user.db")

c = conn.cursor()

# c.execute(""" CREATE TABLE users (
#          first text,
#          last text,
#          pay integer
#          ) """)

# c.execute("INSERT INTO users VALUES ('Osayi', 'Owie', 50000)")

c.execute("SELECT * FROM users WHERE last='Owie'")

print(c.fetchall())

conn.commit()
conn.close()
import sqlite3
import hashlib


conn=sqlite3.connect('rdp_db.db')
cur=conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS usersdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

#username=input('username:')
#password=input('password:')

#cur.execute("INSERT INTO usersdata (username,password) VALUES (?,?)",(username,hashlib.sha256(password.encode()).hexdigest()))

conn.commit()
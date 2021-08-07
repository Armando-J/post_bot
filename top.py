import sqlite3


def ini_bd():
    return sqlite3.connect('anime.bd')


conn = ini_bd()
cursor = conn.cursor()
l = cursor.execute("SELECT id,aport FROM usuarios").fetchall()

conn.commit()
conn.close()


print(l)


f = open('top.txt', 'w')
f.write('')
f.close()






import pickle
import psycopg2
from os import environ

try:
    from secure.s_view_counter import database_url
    database_url()
except:pass

DATABASE_URL=environ['DATABASE_URL']

class Temp():
    def __init__(self):
        self.markup=None

class P_Anime():
    def __init__(self):
        self.titulo = ''
        self.imagen = None
        self.tipo='#Desconocido'
        self.format = ''
        self.status = ''
        self.episodes = ''
        self.genero = ''
        self.descripcion = ''
        self.episo_up = ''
        self.temporada = ''
        self.audio = ''
        self.link = ''
        self.txt=''
        self.inf=''
        self.tomos=''
        self.plata=''
        self.estudio=''
        self.idioma=''
        self.duracion=''
        self.volumen=''
        self.creador=''
        self.version=''
        self.peso=''
        self.sis_j=''

def ini_bd():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = conn.cursor()
    return conn, cursor

def get_u(id,cursor):

    cursor.execute("SELECT id FROM usuarios WHERE id=%s;", (id,))
    l =cursor.fetchone()

    if l:
        return True
    else:
        return False

def new_u(id,temp,conn,cursor):
    try:
        l=(id,pickle.dumps(temp),0)

        cursor.execute("INSERT INTO usuarios (id, temp, aport) VALUES (%s ,%s,%s);", l)

        conn.commit()

    except :
        return False
    else:return True

def set_temp(id,temp):
    conn,cursor=ini_bd()

    cursor.execute("UPDATE usuarios SET temp=%s WHERE id=%s;", (pickle.dumps(temp), id))

    conn.commit()
    cursor.close()
    conn.close()

def get_temp(id):
    conn,cursor = ini_bd()

    cursor.execute("SELECT temp FROM usuarios WHERE id=%s;", (id,))
    l = cursor.fetchone()
    cursor.close()
    conn.close()
    if l:
        return pickle.loads(l[0])
    else:#esta por gusto esto
        new_u(id,Temp())
        get_temp(id)
        return False

def aport(id):
    conn,cursor = ini_bd()

    cursor.execute("UPDATE usuarios SET aport=aport+1 WHERE id=%s;", (id,))

    conn.commit()
    cursor.close()
    conn.close()

def get_aport(id):
    conn,cursor = ini_bd()

    cursor.execute("SELECT aport FROM usuarios WHERE id=%s;", (id,))
    l = cursor.fetchone()

    cursor.close()
    conn.close()
    return l[0]

'''def new_p(id_sms,id_user,titulo):
    l=(time()//3600,id_sms,id_user,titulo)
    conn,cursor = ini_bd()

    cursor.execute("INSERT INTO posts (time ,id_sms ,id_user , titulo) VALUES (%s ,%s,%s,%s);", l)

    conn.commit()
    cursor.close()
    conn.close()

def del_post(id_sms):
    try:
        conn,cursor = ini_bd()

        cursor.execute("DELETE FROM posts WHERE id_sms=%s;", (id_sms,))

        conn.commit()
        cursor.close()
        conn.close()
    except :
        cursor.close()
        conn.close()
        return False
    else:return True'''


conn,cursor=ini_bd()

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY, temp Bytea ,aport INTEGER);''')

"""cursor.execute('''CREATE TABLE IF NOT EXISTS posts
             (id_post SERIAL PRIMARY KEY,time INTEGER ,id_sms INTEGER, id_user INTEGER, titulo TEXT);''') """

conn.commit()
cursor.close()
conn.close()

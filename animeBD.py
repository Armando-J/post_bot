import sqlite3,pickle
from time import time

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
    return sqlite3.connect('anime.bd')

def get_u(id):
    conn = ini_bd()
    cursor = conn.cursor()

    l = cursor.execute("SELECT id FROM usuarios WHERE id=?", (id,)).fetchone()
    conn.close()
    if l:
        return True
    else:
        return False

def new_u(id,temp):
    try:
        l=(id,pickle.dumps(temp),0)
        conn = ini_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios VALUES (?,?,?)",l)
        conn.commit()
        conn.close()
    except :
        conn.close()
        return False
    else:return True

def set_temp(id,temp):
    conn=ini_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET temp=? WHERE id=?", (pickle.dumps(temp), id))
    conn.commit()
    conn.close()

def get_temp(id):
    conn = ini_bd()
    cursor = conn.cursor()
    l = cursor.execute("SELECT temp FROM usuarios WHERE id=?", (id,)).fetchone()
    conn.close()
    if l:
        return pickle.loads(l[0])
    else:
        new_u(id,Temp())
        get_temp(id)
        return False


def aport(id):
    conn = ini_bd()
    cursor = conn.cursor()
    l = cursor.execute("SELECT aport FROM usuarios WHERE id=?", (id,)).fetchone()[0]
    cursor.execute("UPDATE usuarios SET aport=? WHERE id=?", (l+1, id))
    conn.commit()
    conn.close()

def get_aport(id):
    conn = ini_bd()
    cursor = conn.cursor()
    l = cursor.execute("SELECT aport FROM usuarios WHERE id=?", (id,)).fetchone()[0]
    conn.close()
    return l

def new_p(id_sms,id_user,titulo):
    l=(time()//3600,id_sms,id_user,titulo)
    conn = ini_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts VALUES (null,?,?,?,?)",l)
    conn.commit()
    conn.close()

def del_post(id_sms):
    try:
        conn = ini_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id_sms=?", (id_sms,))
        conn.commit()
        conn.close()
    except :
        conn.close()
        return False
    else:return True

def get_resumen():
    conn = ini_bd()
    cursor = conn.cursor()
    l = cursor.execute("SELECT id_sms,titulo FROM posts WHERE ?-time < 25",(time()//3600,)).fetchall()
    conn.close()
    return l

def get_id_re():
    conn = ini_bd()
    cursor = conn.cursor()
    l = cursor.execute("SELECT id_sms FROM generales ").fetchone()
    conn.close()
    return l[0] if l else l

def set_id_re(id_sms):
    try:
        conn = ini_bd()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE generales')
        cursor.execute('''CREATE TABLE IF NOT EXISTS generales
                     (id_sms INTEGER)''')

        cursor.execute("INSERT INTO generales VALUES (?)",(id_sms,))
        conn.commit()
        conn.close()
    except :
        conn.close()
        return False
    else:return True




conn=ini_bd()
cursor=conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id text PRIMARY KEY, temp Binary ,aport INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS posts
             (id_post INTEGER PRIMARY KEY AUTOINCREMENT,time INTEGER ,id_sms INTEGER, id_user INTEGER, titulo TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS generales
             (id_sms INTEGER)''')

conn.close()
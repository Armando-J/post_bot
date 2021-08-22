import anilist,telebot,emoji,animeBD,traceback,re
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from time import sleep

try:
    from secure import post_bot
    id_canal = post_bot.id_canal
    usercanal = post_bot.usercanal
    API_TOKEN = post_bot.API_TOKEN
except:
    import os
    id_canal = os.environ['ID_CANAL']
    usercanal = os.environ['USERCANAL']
    API_TOKEN = os.environ['TOKEN']


def icono(text=''):
    return emoji.emojize(text, use_aliases=True)


bot = telebot.TeleBot(API_TOKEN)

tipD = {'a': 'ANIME', 'm': 'MANGA'}
boton_empezar=icono('/Empezar')
t_i=icono('	:writing_hand: Ingrese el título de la multimedia a subir o presione /cancelar para salir.')
t_ty=icono(':white_check_mark: Seleccione la categoría en que se encuentra la multimedia.')
t_pre=icono('Hola {0} :wave:, este es un bot para ayudarte a publicar en el canal @{1}.\n\nPara comenzar presione :point_right: {2}')
boton_cancelar='/cancelar'
boton_sigui=icono('Siguiente :next_track_button:')
boton_selec=icono('Seleccionar :white_check_mark:')

salir_menu=icono(':house: Salir')
buscar_n=icono(':arrow_right_hook: Volver a buscar con otro texto')
t_cap=icono(':writing_hand: Escriba los cap o el fragmento que contiene el link/txt a subir.\n\n<code> cap 1 - cap 33</code>\n<code>Completo</code>\n<code>Primera parte</code>  etc)\n\no presione /cancelar para salir.')
t_l=icono(':link: Envíe el link o presione /finalizar')
t_el=icono(':dizzy_face: Error! repita de nuevo la función anterior{0}.')
t_at=icono(':memo: Envíe ahora el archivo txt o presione /finalizar para enviar al canal.')
t_li=icono(':dizzy_face: Link incorrecto, por favor vuelva a enviarlo correctamente o presione /cancelar para salir.')
t_ela=icono(':link: Ponga el link s3 del txt.\nEste se obtiene enviando el txt a toDus o de la misma forma que envió las partes.')
t_ad=icono(':expressionless: Lo sentimos, debe ser miembro del canal @{0} para poder usar el bot.\n\n/Empezar'.format(usercanal))

def acceso(id):
    m = bot.get_chat_member(id_canal, id).status
    # “creator”, “administrator”, “member”, “restricted”, “left” or “kicked”
    if m == 'member' or m == 'creator' or m == 'administrator':
        return True
    else:
        try:bot.send_message(id,t_ad)
        except:print(traceback.format_exc())
        return False

def inicio(id):
    if acceso(id):
        try:sms = bot.send_message(id, t_i)
        except:
            print(traceback.format_exc())
        bot.register_next_step_handler(sms, titulo)

def introducc(id,name):
    try:bot.send_message(id, t_pre.format(name,usercanal,boton_empezar))
    except:
        print(traceback.format_exc())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn,cursor=animeBD.ini_bd()

    if not animeBD.get_u(message.chat.id,cursor):
        animeBD.new_u(message.chat.id,animeBD.Temp(),conn,cursor)

    cursor.close()
    conn.close()

    introducc(message.chat.id,message.chat.first_name)

@bot.message_handler(commands=[boton_empezar[1:]])
def send_welcome(message):
    inicio(message.chat.id)

def titulo(message):
    if message.text==boton_cancelar:
        introducc(message.chat.id,message.chat.first_name)
    else:
        temp=animeBD.get_temp(message.chat.id)
        if temp:
            temp.titulo=message.text
            temp.username=message.chat.username
            temp.id_user=message.chat.id
            temp.name=message.chat.first_name
            temp.post=animeBD.P_Anime()
            animeBD.set_temp(message.chat.id,temp)

            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton('Anime', callback_data='a'))
            markup.row(InlineKeyboardButton('Manga', callback_data='m'))
            #markup.row(InlineKeyboardButton('Juego', callback_data='j'))
            markup.row(InlineKeyboardButton('Otro contenido', callback_data='o'))
            markup.row(InlineKeyboardButton(salir_menu, callback_data='s'))
            try:bot.send_message(message.chat.id, t_ty, reply_markup=markup)
            except:
                print(traceback.format_exc())
        else:introducc(message.chat.id,message.chat.first_name)

def error_Html(text):
    if type(text)== str:
        return text.replace('<','')
    else:return ''

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    introducc(message.chat.id,message.chat.first_name)

def post_s(id,temp,index):
    '''{'id': 30012,
                    'title': {'romaji': 'BLEACH'},
                    'format': 'MANGA',
                    'coverImage': {'large': 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/bx30012-z7U138mUaPdN.png'}}, {'id': 41330, 'title': {'romaji': 'Bleach Short Story Edition'}, 'format': 'ONE_SHOT', 'coverImage': {'large': 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/11330.jpg'}}'''
    if (temp.search):
        t=temp.search[index]['title']['romaji']
        f=temp.search[index]['format']
        l=temp.search[index]['coverImage']['extraLarge']

        capt = '<b>{0}\n\nFormato: {1}</b>'.format(error_Html(t), f)
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(boton_sigui,
                                        callback_data='s^{0}'.format(index+1 if index<len(temp.search)-1 else 0)),
                   InlineKeyboardButton(boton_selec,
                                        callback_data='i^{0}'.format(temp.search[index]['id']))
                   )

        markup.row(InlineKeyboardButton(buscar_n,
                                        callback_data='b'))
        markup.row(InlineKeyboardButton(salir_menu,
                                        callback_data='s'))
        try:bot.send_photo(id,l, capt, parse_mode='html',reply_markup=markup)
        except:
            print(traceback.format_exc())
    else:
        try:bot.send_message(id ,'No se encontraron Resultados')
        except:
            print(traceback.format_exc())
        post_e(temp,id,markup_e())

def markup_e():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Editar Título', callback_data='e^n'),
               InlineKeyboardButton('Editar Episodios', callback_data='e^e'))

    markup.row(InlineKeyboardButton('Editar Tipo', callback_data='e^t'),
               InlineKeyboardButton('Editar Formato', callback_data='e^f'))

    markup.row(InlineKeyboardButton('Editar Temporada', callback_data='e^m'),
               InlineKeyboardButton('Editar Audio', callback_data='e^a'))

    markup.row(InlineKeyboardButton('Editar Géneros', callback_data='e^g'),
               InlineKeyboardButton('Editar Estado', callback_data='e^s'))

    markup.row(InlineKeyboardButton('Editar Sinopsis', callback_data='e^i'),
               InlineKeyboardButton('Editar Imagen', callback_data='e^im'))

    markup.row(InlineKeyboardButton('Editar Información', callback_data='e^in'),
               InlineKeyboardButton(icono(':heavy_plus_sign: Màs Categorías :heavy_plus_sign:'), callback_data='m^2'))


    markup.row(InlineKeyboardButton(salir_menu, callback_data='s'),InlineKeyboardButton(boton_sigui, callback_data='e^c'.format()))
    return markup

def markup_e1():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Editar Tomo', callback_data='e^to'),
               InlineKeyboardButton('Editar Plataforma', callback_data='e^p'))

    markup.row(InlineKeyboardButton('Editar Estudio', callback_data='e^es'),
               InlineKeyboardButton('Editar Idioma', callback_data='e^id'))

    markup.row(InlineKeyboardButton('Editar Duración', callback_data='e^d'),
               InlineKeyboardButton('Editar Volumen', callback_data='e^v'))

    markup.row(InlineKeyboardButton('Editar Versión', callback_data='e^ve'),
               InlineKeyboardButton('Editar Peso', callback_data='e^pe'))

    markup.row(InlineKeyboardButton('Editar Creador', callback_data='e^cr'),
               InlineKeyboardButton('Editar Sis de Juego', callback_data='e^sj'))

    markup.row(InlineKeyboardButton(icono(':heavy_plus_sign: Màs Categorías :heavy_plus_sign:'), callback_data='m^1'))


    markup.row(InlineKeyboardButton(salir_menu, callback_data='s'),InlineKeyboardButton(boton_sigui, callback_data='e^c'.format()))
    return markup

def filter(text: str):
    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    username_regex = r"\B@\w+"
    t_me_link = r"t\.me\/[-a-zA-Z0-9.]+(\/\S*)?"

    if re.match(url_regex, text) or re.search(username_regex, text) or re.search(t_me_link, text):
        return False

    return True

def editar(message,t,temp):
    if message.text==boton_cancelar:
        introducc(message.chat.id,message.chat.first_name)
    else:
        if message.text=='/borrar':
            var=None
        else: var=error_Html(message.text)
        if message.content_type == 'text':

            if var and not filter (var):
                bot.send_message(message.chat.id, 'No se permite url ni user_name.')
                sleep(2)
                post_e(temp,message.chat.id,temp.markup if temp.markup else markup_e())
                return

            def add_var(t,var):
                if t=='n':
                    temp.post.titulo=var
                elif t=='e':
                    temp.post.episodes = var
                elif t=='m':
                    temp.post.temporada=var
                elif t=='a':
                    temp.post.audio=var
                elif t=='g':
                    temp.post.genero=var
                elif t=='s':
                    temp.post.status=var
                elif t=='i':
                    temp.post.descripcion=var
                elif t=='t':
                    temp.post.tipo=var
                elif t=='f':
                    temp.post.format=var
                elif t=='in':
                    temp.post.inf=var
                elif t=='to':
                    temp.post.tomos=var
                elif t=='p':
                    temp.post.plata=var
                elif t=='es':
                    temp.post.estudio=var
                elif t=='id':
                    temp.post.idioma=var
                elif t=='d':
                    temp.post.duracion=var
                elif t=='v':
                    temp.post.volumen=var
                elif t=='ve':
                    temp.post.version=var
                elif t=='pe':
                    temp.post.peso=var
                elif t=='cr':
                    temp.post.creador=var
                elif t=='sj':
                    temp.post.sis_j=var
                elif t=='im':temp.post.imagen=None

            add_var(t,var)

            if temp.post.imagen:
                caracteres = len(make_message_body(temp))

                if caracteres > 1024:
                    bot.send_message(message.chat.id, 'Mucho texto !!! Vuelva a intentarlo editando lo mismo pero con {0} letras de menos.'.format(caracteres-1024))
                    sleep(2)
                    add_var(t,None)#borra la variable añadida
                    post_e(temp, message.chat.id, temp.markup if temp.markup else markup_e())
                    return

        elif t=='im' and message.content_type == 'photo':
            temp.post.imagen = message.photo[0].file_id


        animeBD.set_temp(message.chat.id,temp)
        post_e(temp,message.chat.id,temp.markup if temp.markup else markup_e())

def make_message_body(temp: animeBD.Temp):
    tt = []

    def aj(txt, var):
        if var: tt.append(txt.format(var))

    tit = ':radioactive:{0} {1}\n\n'.format(
        '({0})'.format(temp.post.tipo[0]) if temp.post.tipo else '',
        '<b>{0}</b>'.format(temp.post.titulo) if temp.post.titulo else ':expressionless:')

    tt.append(tit)
    aj(':heavy_check_mark:Tipo: <b>{0}</b>\n', temp.post.tipo)
    aj(':heavy_check_mark:Formato: <b>{0}</b>\n', temp.post.format)
    aj(':heavy_check_mark:Episodios: <b>{0}</b>\n', temp.post.episodes)
    aj(':heavy_check_mark:Temporada: <b>{0}</b>\n', temp.post.temporada)
    aj(':heavy_check_mark:Tomo: <b>{0}</b>\n', temp.post.tomos)
    aj(':heavy_check_mark:Volumen: <b>{0}</b>\n', temp.post.volumen)
    aj(':heavy_check_mark:Plataforma: <b>{0}</b>\n', temp.post.plata)
    aj(':notes:Audio: <b>{0}</b>\n', temp.post.audio)
    aj(':heavy_check_mark:Idioma: <b>{0}</b>\n', temp.post.idioma)
    aj(':hourglass_flowing_sand:Duración: <b>{0}</b>\n', temp.post.duracion)
    aj(':heavy_check_mark:Géneros: <b>{0}</b>\n',
       ' '.join(temp.post.genero) if type(temp.post.genero) == list else temp.post.genero)
    aj(':heavy_check_mark:Estudio: <b>{0}</b>\n', temp.post.estudio)
    aj(':heavy_check_mark:Sistema de juego: <b>{0}</b>\n', temp.post.sis_j)
    aj(':floppy_disk:Peso: <b>{0}</b>\n', temp.post.peso)
    aj(':heavy_check_mark:Versión: <b>{0}</b>\n', temp.post.version)
    aj(':heavy_check_mark:Creador: <b>{0}</b>\n', temp.post.creador)
    aj(':heavy_check_mark:Estado: <b>{0}</b>\n', temp.post.status)
    aj('\n:beginner:Sinopsis: <b>{0}</b>\n',
       '{0}...'.format(temp.post.descripcion[:500]) if temp.post.descripcion and len(
           temp.post.descripcion) > 200 else temp.post.descripcion)
    aj('\n\n:warning:Información: <b>{0}</b>\n', temp.post.inf)
    tt.append('\n:star:Aporte #{0} de {1}'.format(
        animeBD.get_aport(temp.id_user) + 1, '@' + temp.username if temp.username else temp.name))
    if temp.post.link: tt.append(
        '\n\n:link:Link: <a href="{0}"><b>{1}</b></a>'.format(temp.post.link, temp.post.episo_up))

    return icono(''.join(tt))

def post_e(temp,id,markup=None):
    capt = make_message_body(temp)
    try:
        if temp.post.imagen:

            try:vvvv=bot.send_photo(id, temp.post.imagen, capt, parse_mode='html', reply_markup=markup).id
            except:
                print(traceback.format_exc())
            return vvvv

        else:
            try:vvvv=bot.send_message(id, capt, parse_mode='html', reply_markup=markup,disable_web_page_preview=True).id
            except:
                print(traceback.format_exc())
            return vvvv
    except:print(traceback.format_exc())

def txtlink(message,temp):
    def finalizar():
        id_sms = post_e(temp, id_canal)
        if temp.post.txt:
            try:bot.send_document(id_canal, temp.post.txt,caption=temp.post.episo_up,parse_mode='html')
            except:
                print(traceback.format_exc())
        try:bot.send_message(message.chat.id, icono('<a href="https://t.me/{0}/{1}">:white_check_mark: <b>Enviado al canal :exclamation:</b></a>\n\nPresione {2} para crear otro post.'.format(usercanal,id_sms,boton_empezar)),parse_mode='html',disable_web_page_preview=True)
        except:
            print(traceback.format_exc())
        animeBD.aport(message.chat.id)
        #animeBD.new_p(id_sms,message.chat.id,temp.post.titulo)


    if message.content_type == 'text':

        if message.text=='/finalizar' and temp.post.link:
            finalizar()
        elif message.text=='/cancelar':
            introducc(message.chat.id,message.chat.first_name)

        elif 'HTTP://S3.TODUS.CU/' == message.text.upper()[:19] or 'HTTPS://S3.TODUS.CU/' == message.text.upper()[:20] :
            temp.post.link=message.text
            animeBD.set_temp(message.chat.id, temp)

            try:sms = bot.send_message(message.chat.id, t_at)
            except:
                print(traceback.format_exc())
            bot.register_next_step_handler(sms, txtlink, temp)

        elif temp.post.link:
            try:sms=bot.send_message(message.chat.id,t_at)
            except:
                print(traceback.format_exc())
            bot.register_next_step_handler(sms, txtlink, temp)

        else:
            try:sms=bot.send_message(message.chat.id,t_li)
            except:
                print(traceback.format_exc())
            bot.register_next_step_handler(sms, txtlink, temp)

    elif message.content_type == "document" and temp.post.link:
        temp.post.txt = message.document.file_id
        #temp.post.name_txt=message.document.file_name
        animeBD.set_temp(message.chat.id, temp)
        finalizar()

    else:
        try:sms = bot.send_message(message.chat.id, t_el.format(
            ' o presione /finalizar para enviar al canal.' if temp.post.link else '' ))
        except:
            print(traceback.format_exc())
        bot.register_next_step_handler(sms, txtlink, temp)

def capsub(message,temp):
    if message.text==boton_cancelar:
        introducc(message.chat.id,message.chat.first_name)
    else:
        temp.post.episo_up=error_Html(message.text)
        animeBD.set_temp(message.chat.id,temp)
        try:sms = bot.send_message(message.chat.id, t_ela)
        except:
            print(traceback.format_exc())
        bot.register_next_step_handler(sms, txtlink,temp)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.delete_message(call.from_user.id, call.message.message_id)
    except Exception as e:
            print('error borrar\n{0}'.format(e))

    else:
        temp=animeBD.get_temp(call.from_user.id)
        if temp:
            data = call.data.split('^')
            l=len(data)
            if l==1:
                temp.tipo=data[0]

                if data[0]=='s':
                    introducc(call.from_user.id,call.from_user.first_name)
                elif data[0]=='b':
                    inicio(call.from_user.id)

                else:
                    if data[0]=='a' or data[0]=='m':
                        d = anilist.search(temp.titulo, data[0])
                        temp.search=d
                        post_s(call.from_user.id,temp,0)
                    elif data[0]=='o':
                        temp.post.titulo=error_Html(temp.titulo)
                        post_e(temp, call.from_user.id, markup_e())

                    animeBD.set_temp(call.from_user.id, temp)



            elif l==2:
                if data[0]=='s':
                    post_s(call.from_user.id,temp,int(data[1]))
                elif data[0]=='i':
                    p=anilist.get(data[1])
                    """{'coverImage': 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/bx30106-GgFOXeyB70xj.png', 
                    'title': 'Cardcaptor Sakura', 
                    'format': 'MANGA', 
                    'status': 'FINISHED', 
                    'episodes': None, 
                    'genres': ['#Adventure', '#Comedy', '#Fantasy', '#Mahou Shoujo', '#Romance'], 
                    'description': 'El cuarto grado Sakura Kinomoto encuentra un libro ...)'}"""
                    temp.search=None
                    temp.titulo=''

                    temp.post = animeBD.P_Anime()
                    temp.post.tipo = tipD[temp.tipo]
                    temp.tipo=''
                    temp.post.imagen=p['coverImage']
                    temp.post.titulo=error_Html(p['title'])
                    temp.post.format=p['format']
                    temp.post.status=p['status']
                    temp.post.episodes=p['episodes']
                    temp.post.genero=p['genres']
                    temp.post.descripcion=error_Html(p['description'])

                    animeBD.set_temp(call.from_user.id,temp)

                    post_e(temp,call.from_user.id,markup_e())

                elif data[0]=='e':
                    if data[1]=='c':

                        try:sms = bot.send_message(call.from_user.id, t_cap,parse_mode='html')
                        except:
                            print(traceback.format_exc())
                        bot.register_next_step_handler(sms, capsub,temp)
                    else:
                        try:sms=bot.send_message(call.from_user.id, 'Envíe los nuevos datos o presione /borrar para borrar esa categoría.')
                        except:
                            print(traceback.format_exc())
                        bot.register_next_step_handler(sms, editar,data[1],temp )
                elif data[0]=='m':
                    markup=None
                    if data[1]=='1':markup=markup_e()
                    else:markup=markup_e1()
                    temp.markup=markup
                    animeBD.set_temp(call.from_user.id,temp)
                    post_e(temp, call.from_user.id,markup)


        else:introducc(call.from_user.id,call.from_user.first_name)

def inicio_bot():
    if usercanal and API_TOKEN and id_canal:

        print('-----------------------\nBot iniciado\n-----------------------')

        try:
            bot.polling(none_stop=True)
        except:print(traceback.format_exc())

if __name__ == '__main__':inicio_bot()

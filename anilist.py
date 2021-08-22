try:
    import ujson as json
except:
    import json
import re,requests
from googletrans import Translator
from time import sleep


url = 'https://graphql.anilist.co'


def search(name: str, MediaType: str):
    t = {'a': 'ANIME', 'm': 'MANGA'}
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            media (id: $id, type: ''' + t[MediaType] + ''', search: $search) {
                id
                title {
                    romaji
                }
                format
                coverImage{
                    extraLarge
                }
            }
        }
    }'''

    variables = {
        'search': name,
        'page': 1,
        'perPage': 8,
        'MediaType': MediaType
    }

    try:
        response = requests.post(
        url, json={'query': query, 'variables': variables})
    except Exception as e:
        print('search',e)
        return False
    # print(response.text)
    else:

        if response.status_code==200:
            try:return list(x for x in json.loads(response.text)['data']['Page']['media'])
            except Exception as e:
                print('search',e)
                return False
        else:
            print('search estatus code',response.status_code)
            return False


def get(id):
    query = '''
	query ($id: Int){
	Media (id: $id){
        coverImage{
            extraLarge
        }
		title {
		romaji		
		}
		format
		status
		episodes
		genres
		description
	}
	}
	'''

    variables = {
        'id': id
    }


    try:
        # Make the HTTP Api request
        response = requests.post(
            url, json={'query': query, 'variables': variables})
        if response.status_code==200:
            raw_response = json.loads(response.text)

            def traducir(texto):

                tr = Translator()
                cont = 0
                while cont < 5:
                    try:
                        return tr.translate(texto, dest='es').text
                    except Exception as e:
                        print('search',e)
                        cont += 1
                        tr = Translator()
                        sleep(1)

                return texto

            info = {
                'coverImage': raw_response['data']['Media']['coverImage']['extraLarge'],
                'title': raw_response['data']['Media']['title']['romaji'] ,
                'format': raw_response['data']['Media']['format'],
                'status': raw_response['data']['Media']['status'],
                'episodes': raw_response['data']['Media']['episodes'],
                'genres': ['#{0}'.format(x).replace(' ','_').replace('-','_') for x in raw_response['data']['Media']['genres']],
                'description': traducir(str(re.sub('<.*?>', '', raw_response['data']['Media']['description']))) if raw_response['data']['Media']['description'] else '',
            }

            return info
        else :
            print('get',response.status_code)
            return False
    except Exception as e:
        print('get',e)
        return False


if __name__ == '__main__':
    print(search('neverland', 'a'))
    '''
    [{'id': 20, 'title': {'romaji': 'Naruto'}, 'format': 'TV'},
    {'id': 21220, 'title': {'romaji': 'Boruto: Naruto the Movie'}, 'format': 'MOVIE'},
    {'id': 3480, 'title': {'romaji': 'Nayuta'}, 'format': 'OVA'},
    {'id': 6000, 'title': {'romaji': 'Haruwo'}, 'format': 'OVA'},
    {'id': 97938, 'title': {'romaji': 'Boruto: Naruto Next Generations'}, 'format': 'TV'}]
    '''
    print(search('naruto', 'm'))
    '''
    [{'id': 36444, 'title': {'romaji': 'Naruto'}, 'format': 'ONE_SHOT'},
    {'id': 30011, 'title': {'romaji': 'Naruto'}, 'format': 'MANGA'},
    {'id': 44573, 'title': {'romaji': 'Karasu Tengu Kabuto'}, 'format': 'MANGA'},
    {'id': 92527, 'title': {'romaji': 'Kiruto'}, 'format': 'MANGA'},
    {'id': 96070, 'title': {'romaji': 'Kiruto'}, 'format': 'MANGA'}]
    '''
    print(get(113415))  # naruto anime
    '''
    {'coverImage': 'https://s4.anilist.co/file/anilistcdn/media/anime/cover/small/nx20-KCjCtnUTsLcu.jpg',
    'title': 'Naruto (ナルト)',
    'format': 'TV',
    'status': 'FINISHED',
    'episodes': 220,
    'genres': ['Action', 'Comedy'],
    'description': "Naruto Uzumaki, un ninja hiperactivo y de nudillos, vive en Konohagakure, el pueblo de hojas ocultas.Momentos antes de su nacimiento, un enorme demonio conocido como el Kyuubi, el zorro de nueve colas, atacó a Konohagakure y causó estragos.Para poner fin al alboroto de Kyuubi, el líder del pueblo, el 4º Hokage, sacrificó su vida y selló la bestia monstruosa dentro del recién nacido Naruto.\nEmitido debido a la presencia del Kyuubi dentro de él, Naruto lucha por encontrar su lugar en el pueblo.Se esfuerza por convertirse en el Hokage de Konohagakure, y él conoce a muchos amigos y enemigos en el camino.\n[Escrito por mal reescritura]"}
    '''
    print(get(30011))  # naruto manga

    '''
    {'coverImage': 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/small/nx30011-9yUF1dXWgDOx.jpg',
    'title': 'Naruto (ナルト)',
    'format': 'MANGA',
    'status': 'FINISHED',
    'episodes': None,
    'genres': ['Action', 'Adventure'],
    'description': 'Antes del nacimiento de Naruto, un gran demonio Fox había atacado el pueblo de hojas ocultas.Un hombre conocido como el 4to Hokage selló al demonio dentro de Naruto recién nacido, lo que le hizo que crezcan sin saberlo detestado por sus compañeros aldeanos.A pesar de su falta de talento en muchas áreas de Ninjutsu, Naruto se esfuerza por un solo objetivo: obtener el título de Hokage, el Ninja más fuerte en su pueblo.Deseando el respeto que nunca recibió, Naruto trabaja hacia su sueño con compañeros de amigos Sasuke y Sakura y Mentor Kakashi, ya que pasan por muchas pruebas y batallas que vienen con ser un ninja.'}
    '''

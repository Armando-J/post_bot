from googletrans import Translator
from time import sleep


def traducir(texto):
    tr = Translator()
    cont = 0
    while cont < 5:
        try:
            return tr.translate(texto, dest='es').text
        except Exception as e:
            print('search', e)
            cont += 1
            tr = Translator()
            sleep(1)

    return texto

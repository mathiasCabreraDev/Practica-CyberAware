import csv
import unicodedata
import os

#RUTAS
import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/k-cmpProject/config.ini')
TWEETS_DATA = config['TWEETS']['TWEETS_DATA']
COMBINADOS = config['TWEETS']['COMBINADOS']
HT = config['TWEETS']['HT'].split(',')
class Combinar:
    def __init__(self):
        self.__hashtags = HT
        
    def __limpiar_cadena(self, palabra):
        s1 = palabra.replace("ñ", "nn").replace("Ñ", "NN")
        s2 = unicodedata.normalize("NFKD", s1).encode("ascii","ignore").decode("ascii")
        return s2

    def run(self):
        print('Combinando tweets obtenidos...')
        id_unicos = set()
        with open(COMBINADOS, 'r', newline='') as archivoCreado:
            linea = 0
            contenido = csv.reader(archivoCreado)
            for tweet in contenido:
                if linea == 0:
                    linea += 1
                    continue
                id_unicos.add(tweet[0])

        with open(COMBINADOS, 'w', newline='') as archivoCreado:
            writer = csv.writer(archivoCreado)
            for h in self.__hashtags:
                if os.path.exists(TWEETS_DATA+ h + '.csv'):
                    with open(TWEETS_DATA + h + '.csv', 'r') as archivo:
                        n_linea = 0
                        contenido = archivo.readlines()
                        for linea in contenido:
                            if n_linea == 0:
                                n_linea += 1
                                continue
                            else:
                                linea = linea.split(',')
                                if linea[0] not in id_unicos and len(linea) == 12:
                                    linea[2] = self.__limpiar_cadena(linea[2])
                                    linea[7] = self.__limpiar_cadena(linea[7])
                                    linea[6] = self.__limpiar_cadena(linea[6])
                                    linea[-1] = linea[-1].strip()
                                    id_unicos.add(linea[0])
                                    writer.writerow(linea)
        archivoCreado.close()
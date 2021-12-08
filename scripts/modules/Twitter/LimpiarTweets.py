import unicodedata
import re
import csv
from datetime import datetime

#RUTAS
import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/k-cmpProject/config.ini')
LIMPIOS = config['TWEETS']['LIMPIOS']
COMBINADOS = config['TWEETS']['COMBINADOS']

class LimpiarTweets:
    def __init__(self):
        self.__inicio = datetime.now()



    def __limpiar_cadena(self, palabra):
        palabra = palabra.replace("'",'')
        palabra = re.sub(r'http\S+', '', palabra )
        s1 = palabra.replace("ñ", "nn").replace("Ñ", "NN")
        s2 = unicodedata.normalize("NFKD", s1).encode("ascii","ignore").decode("ascii")
        return s2

    #Funcion que elimina caracteres no reconocidos por python
    def __clean_str(self, string):
        string = re.sub(r"\'s", "", string)
        string = re.sub(r"\'ve", "", string)
        string = re.sub(r"n\'t", "", string)
        string = re.sub(r"\'re", "", string)
        string = re.sub(r"\'d", "", string)
        string = re.sub(r"\'ll", "", string)
        string = re.sub(r",", "", string)
        string = re.sub(r"!", " ! ", string)
        string = re.sub(r"\(", "", string)
        string = re.sub(r"\)", "", string)
        string = re.sub(r"\?", "", string)
        string = re.sub(r"'", "", string)
        string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
        string = re.sub(r"[0-9]\w+|[0-9]","", string)
        string = re.sub(r"\s{2,}", " ", string)
        string = re.sub(r'http\S+', '', string)
        return string.strip().lower()

    def run(self):
        print('Limpiado tweets...')
        with open(LIMPIOS, 'w' , newline='') as archivo:
            csv_writer = csv.writer(archivo)
            with open(COMBINADOS, 'r') as combi:
                contenido = combi.readlines()
                for tweet in contenido:
                    tweet = tweet.strip()
                    tweet = tweet.split(',')
                    tweet[2] = self.__limpiar_cadena(tweet[2])
                    tweet[2] = self.__clean_str(tweet[2])
                    if len(tweet[2]) == 0: print (tweet[0])
                    tweet[7] = self.__limpiar_cadena(tweet[7])
                    tweet[7] = self.__clean_str(tweet[7])
                    csv_writer.writerow(tweet)

        print("Tiempo:", datetime.now() - self.__inicio)
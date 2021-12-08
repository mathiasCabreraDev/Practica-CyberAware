import csv
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords
from datetime import datetime

#RUTAS
import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/k-cmpProject/config.ini')
LIMPIOS = config['TWEETS']['LIMPIOS']
STEM = config['TWEETS']['STEM']

inicio = datetime.now()

class StemTweets:
    def __init__(self):
        self.__inicio = datetime.now()
        self.__stopWords = set(stopwords.words())
        self.__ps = nltk.stem.PorterStemmer()


    def __quitarStop(self, tweet):
        nuevo_tweet = list()
        tweet = tweet.strip().split(' ')
        for palabra in tweet:
            if palabra in self.__stopWords: continue
            else: nuevo_tweet.append(palabra)
        nuevo_tweet = ' '.join(nuevo_tweet)
        return nuevo_tweet

    def __stemming(self, tweet):
        nuevo_tweet = list()
        tweet = tweet.strip().split(' ')
        for palabra in tweet:
            palabra = self.__ps.stem(palabra)
            nuevo_tweet.append(palabra)
        nuevo_tweet = ' '.join(nuevo_tweet)
        return nuevo_tweet

    def run(self):
        print('Stemming :)...')
        with open(STEM, 'w', newline = '') as archivo:
            csv_writer = csv.writer(archivo)
            with open(LIMPIOS, 'r') as f:
                contenido = f.readlines()

                for tweet in contenido:
                    tweet = tweet.strip()
                    tweet = tweet.split(',')
                    if 'rt' in tweet[2]: continue
                    tweet[2] = self.__quitarStop(tweet[2])
                    tweet[2] = self.__stemming(tweet[2])
                    if len(tweet[2]) == 0: continue
                    csv_writer.writerow(tweet)
                    
        print("Tiempo:", datetime.now() - self.__inicio)

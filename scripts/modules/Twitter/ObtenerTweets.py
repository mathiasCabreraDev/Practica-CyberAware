import tweepy
import csv
import unicodedata
import os
from datetime import datetime
from dotenv import load_dotenv

#RUTAS
import configparser
config = configparser.ConfigParser()
config.read('/home/str/Desktop/poo/k-cmpPOO/config.ini')
TWEETS_DATA = config['TWEETS']['TWEETS_DATA']
HT = config['TWEETS']['HT'].split(',')

# #CREDENCIALES: configurar en .env
class Twitter:
    def __init__(self):
        load_dotenv()
        self.__consumerKey = os.getenv('CONSUMER_KEY')
        self.__consumerSecret = os.getenv('CONSUMER_SECRET')
        self.__accessToken = os.getenv('ACCESS_TOKEN')
        self.__accessTokenSecret = os.getenv('ACCESS_TOKEN_SECRET') 
        self.__hashtags = HT
        self.__inicio = datetime.now()

    #Funcion que se usa para limpiar la cadena
    def __limpiar_cadena(self, palabra):
        s1 = palabra.replace("ñ", "nn").replace("Ñ", "NN")
        s2 = unicodedata.normalize("NFKD", s1).encode("ascii","ignore").decode("ascii")
        s2 = s2.replace("nn", "ñ"). replace("NN", "Ñ")
        return s2

    #Funcion utilizada para rescatar ultimo tweet agregado al documento. (Parametro utilizado mas adelante)
    def __ultimo_tweet(self, frase):
        with open(TWEETS_DATA+frase+'.csv', 'r') as archivo:
            for tweet in reversed(list(csv.reader(archivo))):
                if len(tweet) == 0 :
                    continue
                if tweet[0] == 'tweet_id': return 1217444742797123584
                return int(tweet[0])

    #Funcion encargada de pedir resultados a la api de tweeter a traves de tweepy.Cursor
    def __resultados(self, api, query, modo, ultima_id):
        if ultima_id != 0:
            results = [status for status in tweepy.Cursor(api.search, q= query, lang = 'en', tweet_mode=modo, max_id=ultima_id-1).items(500)]
            return results
        else:
            results = [status for status in tweepy.Cursor(api.search, q=query, lang = 'en', tweet_mode=modo).items(500)]
            return results

    #Funcion en la cual se reciben los tweets de la funcion anterior y se rescatan los datos importantes
    #en un archivo con el nobre del hashtag y extension csv
    def __obtener_tweets(self, ultima_id, frase):
        auth = tweepy.OAuthHandler(self.__consumerKey, self.__consumerSecret)
        auth.set_access_token(self.__accessToken, self.__accessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        query = '#'+frase
        with open(TWEETS_DATA+frase+'.csv', 'a', newline = '') as archivo:
            escribir = csv.writer(archivo)   
            results = self.__resultados(api, query, 'extended', ultima_id)
            if len(results) == 0: 
                self.__hashtags.remove(frase)
                return
            for tweet in results:
                datos = [
                    tweet.id,
                    tweet.created_at,
                    self.__limpiar_cadena(tweet.full_text.replace('\n',' ').replace(',','.')),
                    tweet.favorite_count,
                    tweet.retweet_count,
                    tweet.user.id,
                    tweet.user.screen_name.replace('\n',' ').replace(',','.'),
                    self.__limpiar_cadena(tweet.user.location.replace('\n',' ').replace(',','.')),
                    tweet.user.followers_count
                    ]
                if (tweet.coordinates != None): 
                    datos.append(tweet.coordinates['coordinates'][0])
                    datos.append(tweet.coordinates['coordinates'][1])
                else :
                    datos.append('None')
                    datos.append('None')
                try:
                    datos.append(tweet.retweeted_status.id)
                except :
                    datos.append('N/A')
                escribir.writerow(datos)
            
    #Funcion en la que se tienen todos los hashtags a buscar que corre de manera permanente hasta que se dejen de 
    #recibir tweets, dentro de esta funcion tambien se crean los archivos que no existen y son necesarios.
    def run(self):
        print('Obteniendo datos desde Twitter...')
        for hashtag in self.__hashtags:
            path = TWEETS_DATA+hashtag+'.csv'
            if os.path.exists(path) :
                os.remove(TWEETS_DATA+hashtag+'.csv')
        for i in range(0,len(self.__hashtags)):
            for hashtag in self.__hashtags:
                path = TWEETS_DATA+hashtag+'.csv'
                if not os.path.exists(path):
                    with open(TWEETS_DATA+hashtag+'.csv', 'w', newline='') as archivo:
                        escribir = csv.writer(archivo)
                        escribir.writerow(['tweet_id','fecha_creacion', 'texto', 'cantidad_likes', 'cantidad_retweet', 'usuario', 'nombre_pantalla', 'ubicacion', 'seguidores','longitud','latitud','id_tweet_original'])
                    self.__obtener_tweets(0, hashtag)
                else:
                    ultima_id = self.__ultimo_tweet(hashtag)
                    self.__obtener_tweets(ultima_id,hashtag)

        print("Tiempo:", datetime.now() - self.__inicio)
        

    
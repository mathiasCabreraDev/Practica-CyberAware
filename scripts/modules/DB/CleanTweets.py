import pandas as pd
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

#RUTAS
import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/k-cmpProject/config.ini')
LIMPIOS = config['TWEETS']['LIMPIOS']

class CleanTweets:
    def __init__(self):
        load_dotenv()
        self.__host = os.getenv('HOST')
        self.__database = os.getenv('DATABASE')
        self.__user = os.getenv('USUARIO')
        self.__password= os.getenv('PASS') 
        self.__inicio = datetime.now()
        self._connection = None

    def __conection(self):
        return mysql.connector.connect(host= self.__host,
                                database= self.__database,
                                user= self.__user,
                                password= self.__password)

    def run(self):
        print('Insertando los tweets limpios a la base de datos...')
        try:
        #conn = psycopg2.connect(database_connection)
            self._connection = self.__conection()
            cur = self._conection.cursor()
            cur.execute("""DELETE FROM tweets""")

            document = list()

            data = pd.read_csv(LIMPIOS)
            a = data['tweet_id'].tolist()
            c = data['texto'].tolist()

            for linea in c:
                document.append(linea)

            for index,tweet in enumerate(document):
                cur.execute("""INSERT INTO tweets(tweet_id,texto) 
                            VALUES(%s,'%s') """ % 
                            (a[index],tweet))
                self._connection.commit()
                
            print("Tiempo:", datetime.now() - self.__inicio)
        
        except:
            print("No pude conectarme a la base de datos")
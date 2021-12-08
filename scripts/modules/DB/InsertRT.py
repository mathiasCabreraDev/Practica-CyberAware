import csv
import mysql.connector
from datetime import datetime
from geocoder import arcgis
from dotenv import load_dotenv
import os

import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/k-cmpProject/config.ini')
LIMPIOS = config['TWEETS']['LIMPIOS']


class InsertRT:
    def __init__(self):
        load_dotenv()
        self.__host = os.getenv('HOST')
        self.__database = os.getenv('DATABASE')
        self.__user = os.getenv('USUARIO')
        self.__password= os.getenv('PASS') 
        self.__startTime = datetime.now()
        self.__connection = None
        self.__cur = None

    def run(self):
        self.__connection = mysql.connector.connect(host= self.__host,
                                                    database = self.__database,
                                                    user= self.__user,
                                                    password= self.__password)

        self.__cur= self.__connection.self.__cursor()

        self.__cur.execute("""DELETE FROM retweets""")

        with open(LIMPIOS , 'r') as f:
            contenido = csv.reader(f, delimiter = ',')
            linea = 0
            for tweet in contenido:
                latitud = 'NULL'
                longitud = 'NULL'
                if linea == 0:
                    linea += 1
                    continue
                if len(tweet[7]) != 0:
                    geo = arcgis(tweet[7]).json
                    if(len(geo) != 0):
                        latitud = geo['lat']
                        longitud = geo['lng']
                if tweet[11] != 'N/A':
                    self.__cur.execute("""INSERT INTO retweets(tweet_id,texto, fecha_creacion, ubicacion, id_tweet_original, longitud, latitude) 
                                VALUES(%s,'%s','%s','%s',%s, %s, %s); """ % 
                                (tweet[0],tweet[2].strip(),tweet[1],tweet[7].strip(),tweet[11], longitud, latitud))
                    self.__connection.commit()
        print("Tiempo:", datetime.now() - self.__startTime)

from datetime import datetime
from scripts.modules.DB.InsertRT import InsertRT
from modules.Twitter.ObtenerTweets import Twitter
from modules.Twitter.Combinar import Combinar
from modules.Twitter.LimpiarTweets import LimpiarTweets
from modules.Twitter.StemTweets import StemTweets
from modules.kcmp.Weight import Weight
from modules.kcmp.k_cpm import Kcmp
from modules.DB.CleanTweets import CleanTweets
from modules.DB.DCinsertDB import DCInsertDB
from modules.mapa.GenerarMapaInicial import GenerarMapa
from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd

load_dotenv()
host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USUARIO')
password= os.getenv('PASS') 

import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/k-cmpProject/config.ini')

LIMPIOS = config['TWEETS']['LIMPIOS']

if __name__ == '__main__':
    Twitter().run()
    Combinar().run()
    LimpiarTweets().run()
    StemTweets().run()
    Weight().run()

    #insert
    conn = mysql.connector.connect(host= host,
                                database= database,
                                user= user,
                                password= password)
    cur = conn.cursor()
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
        conn.commit()
    
    DCInsertDB.run()

from keplergl import KeplerGl
import pandas as pd
import mysql.connector
import sys
from hex_config import config


try:
    #conn = psycopg2.connect(database_connection)
    conn = mysql.connector.connect(host='localhost',
                                   database='cyberaware_copia',
                                   user='cyber',
                                   password='Unab.2021')

except:
    print("No pude conectarme a la base de datos")

def generar_archivo():
    query ="select * from retweets where id_tweet_original = {}".format(sys.argv[1])
    df = pd.read_sql_query(query, con=conn)
    df['fecha_creacion'] = df['fecha_creacion'].astype(str)

    map_1 = KeplerGl()
    map_1.add_data(data=df, name='data_1')
    map_1.config = config
    map_1.save_to_html(data={'data_1': df}, config=config, file_name = 'mapa.html')

generar_archivo()
print('Termine')
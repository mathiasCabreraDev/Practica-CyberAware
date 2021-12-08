import csv
import mysql.connector
from datetime import datetime
import googlemaps


inicio = datetime.now()
gmaps = googlemaps.Client(key='AIzaSyDJhwI0CaCM-YwcIw-Jm1LWW9j2v_yU3gw')

try:
    #conn = psycopg2.connect(database_connection)
    conn = mysql.connector.connect(host='localhost',
                                   database='cyberaware',
                                   user='root',
                                   password='Unab.2019')

except:
    print("No pude conectarme a la base de datos")
cur = conn.cursor()

cur.execute("""DELETE FROM retweets""")

with open('tweetsLimpios.csv' , 'r') as f:
    contenido = csv.reader(f, delimiter = ',')
    linea = 0
    for tweet in contenido:
        latitud = 'NULL'
        longitud = 'NULL'
        if linea == 0:
            linea += 1
            continue
        if len(tweet[7]) != 0:
            geocode_result = gmaps.geocode(tweet[7])
            if(len(geocode_result) != 0):
                r = geocode_result[0]['geometry']['location']
                latitud = r['lat']
                longitud = r['lng']
        if tweet[11] != 'N/A':
            cur.execute("""INSERT INTO retweets(tweet_id,texto, fecha_creacion, ubicacion, id_tweet_original, longitud, latitude) 
                        VALUES(%s,'%s','%s','%s',%s, %s, %s); """ % 
                        (tweet[0],tweet[2].strip(),tweet[1],tweet[7].strip(),tweet[11], longitud, latitud))
            conn.commit()
print("Tiempo:", datetime.now() - inicio)

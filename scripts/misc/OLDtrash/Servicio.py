from flask import  Flask, request, render_template
from flask_restful import Resource, Api
import shutil
from keplergl import KeplerGl
import pandas as pd
import mysql.connector
import sys
from conf_rt import config
import re
import unicodedata
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine

app = Flask(__name__)
api = Api(app)

stop_words = set(stopwords.words('english'))
ps = nltk.stem.PorterStemmer()

def limpiar_cadena(palabra):
    palabra = palabra.replace("'",'')
    s1 = palabra.replace("ñ", "nn").replace("Ñ", "NN")
    #s1 = re.sub(r'http\S+', '', s1 )
    s2 = unicodedata.normalize("NFKD", s1).encode("ascii","ignore").decode("ascii")
    return s2

#Funcion que elimina caracteres no reconocidos por python
def clean_str(string):
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

def quitarStop(tweet):
    nuevo_tweet = list()
    tweet = tweet.strip().split(' ')
    for palabra in tweet:
        if palabra in stop_words: continue
        else: nuevo_tweet.append(palabra)
    nuevo_tweet = ' '.join(nuevo_tweet)
    return nuevo_tweet

def stemming(tweet):
    nuevo_tweet = list()
    tweet = tweet.strip().split(' ')
    for palabra in tweet:
        palabra = ps.stem(palabra)
        nuevo_tweet.append(palabra)
    nuevo_tweet = ' '.join(nuevo_tweet)
    return nuevo_tweet

def calcularDistancia(frase):
    stopwords_stemming_apply = list()
    frase = limpiar_cadena(frase)
    frase = clean_str(frase)
    frase = quitarStop(frase)
    frase = stemming(frase)
    stopwords_stemming_apply.append(frase)
    conn = mysql.connector.connect(host='localhost', database='cyberaware', user='root', password='Unab.2019')
    cur = conn.cursor()
    cur.execute("SELECT * from comunidades")
    rows = cur.fetchall()
    comunidades = list()
    comunidades.append(frase)
    for row in rows:
        comunidades.append(row[2])
    
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(comunidades).toarray()
    matrizComunidades = vectors[1:]

    words = vectorizer.get_feature_names()
    palabras = " ".join(words)
    
    stopwords_stemming_apply.append(palabras)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(stopwords_stemming_apply).toarray()
    vectorFrase = vectors
    print (len(matrizComunidades[0]))
    print (len(vectorFrase[0]))

    menor = 1
    retorno = None
    for index,mc in enumerate(matrizComunidades):
        distancia = cosine(vectorFrase[0],mc)
        if menor > distancia:
            menor = distancia
            retorno = rows[index][0]
    print(retorno)

    return retorno

class Busqueda(Resource):
    def post(self):
        frase = request.form['frase']
        id_comunidad = calcularDistancia(frase)
        if id_comunidad == None:
            id_comunidad = 0
        return id_comunidad

class Bienvenida(Resource):
    def get(self):
        return ('<h1>Hola Mundo!!</h1>')

class Mapa(Resource):
    def get(self, num):
        conn = mysql.connector.connect(host='localhost', database='cyberaware', user='root', password='Unab.2019')

        query ="select * from retweets where id_tweet_original = {}".format(num)
        df = pd.read_sql_query(query, con=conn)
        df['fecha_creacion'] = df['fecha_creacion'].astype(str)

        map_1 = KeplerGl()
        map_1.add_data(data=df, name='data_1')
        map_1.config = config
        map_1.save_to_html(data={'data_1': df}, config=config, file_name = 'mapa1.html')
        
        shutil.copyfile('mapa.html', '/var/www/html/cyberaware/back/tweets/generar/mapa.html')
        return 

api.add_resource(Bienvenida,'/')
api.add_resource(Mapa,'/mapa/<int:num>')
api.add_resource(Busqueda,'/busqueda')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
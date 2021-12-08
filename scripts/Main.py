from datetime import datetime
from scripts.modules.DB.InsertRT import InsertRT
from modules.Twitter.ObtenerTweets import Twitter
from modules.Twitter.Combinar import Combinar
from modules.Twitter.LimpiarTweets import LimpiarTweets
from modules.Twitter.StemTweets import StemTweets
from modules.kcmp.Weight import Weight
from modules.kcmp.k_cpm import Kcmp
from modules.DB.CleanTweets import CleanTweets
from modules.DB.InsertDB import InsertDB
from modules.mapa.GenerarMapaInicial import GenerarMapa
inicio = datetime.now()

#RUTAS
import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/k-cmpProject/config.ini')

DB = config['MODULES']['DB']
KCMP = config['MODULES']['K-CMP']
MAPA = config['MODULES']['MAPA']
TWITTER = config['MODULES']['Twitter'] 

if __name__ == '__main__':
    print('>ObtenerTweets')
    t = Twitter()
    t.run()

    print('\n>Combinar')
    c = Combinar()
    c.run()

    print('\n>LimpiarTweets')
    lt = LimpiarTweets()
    lt.run()

    print('\nStemTweets')
    s = StemTweets()
    s.run()

    print('\nWeight')
    w = Weight()
    w.run()

    print('\nk_cmp')
    kcmp = Kcmp()
    kcmp.run()

    print('\nInsertTweetsLimpios')
    ct = CleanTweets()
    ct.run()

    print('\nInsertDB')
    i = InsertDB()
    i.run()

    print('\nInsertRT')
    rt = InsertRT()
    rt.run()

    print('\nGenerarMapa')
    m = GenerarMapa()
    m.run()
    print("Tiempo TOTAL:", datetime.now() - inicio)

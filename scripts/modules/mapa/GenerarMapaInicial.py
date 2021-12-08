from keplergl import KeplerGl
import pandas as pd
from mapa_bienvenida import config
from pathlib import Path
import shutil

#RUTAS
import configparser
conf = configparser.ConfigParser()
conf.read('/var/www/html/k-cmpProject/config.ini')
LOC_API = conf['MAPA']['LOC_API']
LOC_ARC = conf['MAPA']['LOC_ARC']
MAP = conf['MAPA']['MAP']
BACK = conf['MAPA']['BACK']


class GenerarMapa:
    def __init__(self):
        self.__df = None
        self.__df2 = None
        self.__map = None

    def run(self):
        print('Generando mapa...')
        self.__df= pd.read_csv(LOC_API)

        self.__df2= pd.read_csv(LOC_ARC)
        self.__map = KeplerGl()
        self.__map.add_data(data=self.__df, name='data_1')
        self.__map.add_data(data=self.__df2, name='data_2')
        self.__map.save_to_html(data={'data_1': self.__df, 'data_2': self.__df2}, config=config, file_name=MAP, read_only=False)

        shutil.copyfile(MAP, BACK)

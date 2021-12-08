from datetime import datetime
import networkx as nx
from networkx.algorithms.community import k_clique_communities

import configparser
config = configparser.ConfigParser()
config.read('/var/www/html/k-cmpProject/config.ini')
WEIGHT = config['K_CMP']['WEIGHT']
K_CMP = config['K_CMP']['K_CMP']

class Kcmp:
    def __init__(self):
        self.__inicio = datetime.now()
        self.__graph = nx.Graph()
        self.__L = nx.read_weighted_edgelist(WEIGHT)

    def run(self):
        print('Usando k_cpm.py')
        self.__graph.add_node(1)
        
        k_cpm = list(range(5,11))#5 y 31
        k_cpm.reverse()

        for k in k_cpm:
            print ("Calculando con K: %s" % k)
            c = list(k_clique_communities(self.__L, k))
            with open(K_CMP + str(k) + ".txt","w") as archivo:
                for i in map(list, c):
                    for j in i:
                        archivo.write(str(j) + ' ')
                    archivo.write('\n')
            print("Termine K: {}".format(k))

        print ("Tiempo:", datetime.now() - self.__inicio)
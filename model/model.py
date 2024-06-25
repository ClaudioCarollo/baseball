import copy

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._bestpesoTot = None
        self._bestComp = None
        self._grafo = nx.Graph()
        self._idMap = {}

    def getYear(self):
        anni = DAO.getYear()
        return anni

    def getTeam(self, year):
        teams = DAO.getTeam(year)

        return teams
    def buildgraph(self, year):
        teams = self.getTeam(year)
        self._grafo.add_nodes_from(teams)
        for n1 in self._grafo.nodes:
            self._idMap[n1.code] = n1
            for n2 in self._grafo.nodes:
                if n1.code != n2.code:
                    peso1 = DAO.getSalario(year, n1.code)
                    peso2 = DAO.getSalario(year, n2.code)
                    peso = peso1+peso2
                    if peso>0:
                        self._grafo.add_edge(n1, n2, weight = peso)

    def getpesidecrescenti(self, n):
        pesi = {}
        for n1 in self._grafo.neighbors(n):
            pesi[self._grafo[n][n1]["weight"]] = n1
        pesi_ordinati = dict(sorted(pesi.items(), key=lambda item: item[0], reverse=True))
        return pesi_ordinati

    def getPath(self, s0):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestpesoTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = [s0]
        self._ricorsione(parziale)
        return self._bestComp

    def _ricorsione(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache
        if self._getScore(parziale) > self._bestpesoTot:
            # se lo è aggiorno i valori migliori
            self._bestComp = copy.deepcopy(parziale)
            self._bestpesoTot = self._getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        for a in self._grafo.nodes:
            if len(parziale) == 1 and a not in parziale:
                parziale.append(a)
            if a not in parziale and self._grafo[parziale[-1]][a]["weight"] < self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(a)
                self._ricorsione(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking

    def _getScore(self, listOfNodes):
        peso = 0
        for i in range(0, len(listOfNodes)-1):
            peso += self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return peso


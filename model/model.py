import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap = {}
        self._album = None
        self._myedges = None
        self._grafo = nx.Graph()
        self._bestSet = None
        self._bestScore = 0

    def buildGraph(self, minuti):
        # trova i vertici
        self._album = DAO.getAlbum(minuti)
        self._grafo.clear()
        if len(self._album) == 0:
            print("Lista album vuota.")
            return

        # Aggiungi solo gli ID degli album come nodi
        self._idMap = {t.AlbumId: t for t in self._album}
        self._grafo.add_nodes_from(self._idMap.keys())


        # trova archi
        self._myedges = DAO.getedges(minuti)

        self._grafo.add_edges_from(self._myedges)

    def componenteConnessa(self, v0):
        conn = nx.node_connected_component(self._grafo, v0)
        durata = 0
        for c in conn:
            durata += self._idMap[c].millisecondi
        durata = durata/60000
        return len(conn), durata

    def getSetAlbum(self, a1, dTOT):
        self._bestSet = None
        self._bestScore = 0
        connessa = nx.node_connected_component(self._grafo, a1)
        parziale = set([a1])
        connessa.remove(a1)

        self._ricorsione(parziale, connessa, dTOT)

        return self._bestSet, self.durataTot(self._bestSet)

    def _ricorsione(self, parziale, connessa, dTOT):
        # verificare se parziale è una sol ammissibile
        if self.durataTot(parziale) > dTOT:
            return

        # verificare se parziale è migliore del best
        if len(parziale) > self._bestScore:
            self._bestSet = copy.deepcopy(parziale)
            self._bestScore = len(parziale)

        # ciclo su nodi aggiungibili -- ricorsione
        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                # rimanenti = copy.deepcopy(connessa)
                # rimanenti.remove(c)
                self._ricorsione(parziale, connessa, dTOT)
                parziale.remove(c)

    def durataTot(self, listOfNodes):
        dtot = 0
        for n in listOfNodes:
            dtot += n.totD
        dtot=dtot/60000
        return dtot

    '''
    def getBestSet(self, a1, durataTot):
        self._bestSet = list()
        self._bestScore = 0
        connessa = set(nx.node_connected_component(self._grafo, a1))
        parziale = [self._idMap[a1]]
        connessa.remove(a1)

        self._ricorsione(parziale, connessa, durataTot)

        return self._bestSet, self.getScore(self._bestSet)

    def _ricorsione(self, parziale, connessa, durataTot):
        if self.getScore(parziale) > durataTot: # Verifica se parziale è una soluzione ammissibile
            return

        # Verifica se parziale è migliore del best
        if len(parziale) > self._bestScore:
            self._bestSet = copy.deepcopy(parziale)
            self._bestScore = len(parziale)

        # Ciclo sui nodi aggiungibili -- ricorsione
        for c in list(connessa):  # Usa una copia della lista per iterare
            if self._idMap[c] not in parziale:
                parziale.append(self._idMap[c])
                connessa.remove(c)
                self._ricorsione(parziale, connessa, durataTot)
                parziale.pop()
                connessa.add(c)

    def getScore(self, lista):
        dTot = 0
        for n in lista:
            dTot += n.millisecondi
        dTot = dTot / 60000
        return dTot

    
    def getBestSet(self, a1, durataTot):
        self._bestSet = None
        self._bestScore = 0
        connessa = set(nx.node_connected_component(self._grafo, a1))
        parziale = set([a1])
        connessa.remove(a1)

        self.ricorsione(parziale, connessa, durataTot)

        return self._bestSet, self.getScore(self._bestSet)

    def ricorsione(self, parziale, connessa, durataTot):
        # Verifica se parziale è una soluzione ammissibile
        if self.getScore(parziale) > durataTot:
            return

        # Verifica se parziale è migliore del best
        if len(parziale) > self._bestScore:
            self._bestSet = copy.deepcopy(parziale)
            self._bestScore = len(parziale)

        # Ciclo sui nodi aggiungibili -- ricorsione
        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                self.ricorsione(parziale, connessa, durataTot)
                parziale.remove(c)

    def getScore(self, list):
        dTot = 0
        for n in list:
            dTot += self._idMap[n].millisecondi
        dTot = dTot/60000
        return dTot
    '''



    def printGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)






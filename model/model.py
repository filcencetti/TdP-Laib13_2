import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self.best_driver = None
        self.best_result = 0
        self.k = None
        self.min_rate = 10000
        self.dream_team = []


    def getAllSeasons(self):
        return DAO.getAllSeasons()

    def buildGraph(self,season):
        self._graph.clear()
        allDrivers = DAO.getAllPilots(int(season))
        self._graph.add_nodes_from(allDrivers)
        for driver in allDrivers:
            self._idMap[driver.driverId] = driver

        allEdges = DAO.getAllEdges(int(season))
        for edge in allEdges:
            self._graph.add_edge(self._idMap[edge[0]], self._idMap[edge[1]], weight=edge[2])

    def getBeastDriver(self):
        for node in self._graph.nodes():
            sum = self.getSum(node)
            if sum > self.best_result:
                self.best_result = sum
                self.best_driver = copy.deepcopy(node)

    def getSum(self, node):
        sum = 0
        for nd in self._graph.successors(node):
            sum += self._graph[node][nd]["weight"]

        for nd in self._graph.predecessors(node):
            sum -= self._graph[nd][node]["weight"]

        return sum

    def getDreamTeam(self, K):
        self.k = K
        self.min_rate = 10000
        self.dream_team = []

        parziale = []
        self.recursion(parziale)

    def recursion(self, parziale):
        if len(parziale) == self.k:
            team_rate = self.getRate(parziale)
            if team_rate < self.min_rate:
                self.min_rate = team_rate
                self.dream_team = copy.deepcopy(parziale)
            return

        for node in self._graph.nodes():
            if node not in parziale:
                parziale.append(node)
                self.recursion(parziale)
                parziale.pop()

    def getRate(self, parziale):
        sum = 0
        for node in parziale:
            for nd in self._graph.predecessors(node):
                if nd not in parziale:
                    sum += self._graph[nd][node]["weight"]
        return sum
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import CorCasa
from implementacao import Position


class Lance(object):

    def __init__(self):
        self.linha: int = None
        self.coluna: int = None
        self.empate: str = None
        self.cor: CorCasa = None

    def getLinha(self) -> int:
        return self.linha

    def setLinha(self, linha: int):
        self.linha = linha

    def getColuna(self) -> int:
        return self.coluna

    def setColuna(self, coluna: int):
        self.coluna = coluna

    def getCor(self) -> CorCasa:
        return self.cor

    def setCor(self, cor: CorCasa):
        self.cor = cor

    def getPlayer2(self):
        pass

    def getPosition(self, aLinha: int, aColuna: int) -> Position:
        pass

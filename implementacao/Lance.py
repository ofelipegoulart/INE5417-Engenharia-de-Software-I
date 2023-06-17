#!/usr/bin/python
# -*- coding: UTF-8 -*-
import CorCasa
from implementacao import Position
from implementacao.Peca import Peca


class Lance(object):

    def __init__(self, peca: Peca, linha: int, coluna: int, captura: bool):
        self.linha: int = linha
        self.coluna: int = coluna
        self.peca: Peca = peca
        self.captura: bool = captura

    def getLinha(self) -> int:
        return self.linha

    def setLinha(self, linha: int):
        self.linha = linha

    def getColuna(self) -> int:
        return self.coluna

    def setColuna(self, coluna: int):
        self.coluna = coluna

    def setPeca(self, peca: Peca):
        self.peca = peca

    def getPeca(self) -> Peca:
        return self.peca

    def setCaptura(self, captura: bool):
        self.captura = captura

    def getCaptura(self) -> bool:
        return self.captura

    # def getPlayer2(self):
    #     pass

    # def getPosition(self, aLinha: int, aColuna: int) -> Position:
    #     pass

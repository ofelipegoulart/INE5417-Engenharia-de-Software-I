#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Peca
import CorCasa


class Position(object):

    def __init__(self):
        self.ocupante: Peca = None
        self.casa: CorCasa = None
        self.linha: int = None
        self.coluna: int = None

    def informarOcupada(self, linha: int, coluna: int) -> bool:
        pass

    def informarOcupante(self, linha: int, coluna: int) -> Peca:
        pass

    def getCasa(self) -> CorCasa:
        return self.casa

    def setCasa(self, casa: CorCasa) -> None:
        self.casa = casa

    def getLinha(self) -> int:
        return self.linha

    def setLinha(self, linha: int) -> None:
        self.linha = linha

    def getColuna(self) -> int:
        return self.coluna

    def setColuna(self, coluna: int) -> None:
        self.coluna = coluna

    def validPositions(self) -> list:
        pass

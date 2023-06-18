#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import jsonpickle
import Peca
import CorCasa


class Position(object):

    def __init__(self, linha: int, coluna: int, cor: CorCasa):
        self.ocupante: Peca = None
        self.casa: CorCasa = cor
        self.linha: int = linha
        self.coluna: int = coluna

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

    def getOcupante(self) -> Peca:
        return self.ocupante
    
    def setOcupante(self, ocupante: Peca) -> Peca:
        self.ocupante = ocupante

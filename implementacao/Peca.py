#!/usr/bin/python
# -*- coding: UTF-8 -*-
import CorPeca
import Lance
import Jogador
from typing import List


class Peca(object):
    def __init__(self):
        self.cor: CorPeca = None
        self.dama: bool = False
        self.casa: Lance = None
        self.jogador: Jogador = None

    def getCor(self) -> CorPeca:
        return self.cor

    def setCor(self, cor: CorPeca):
        self.cor = cor

    def getDama(self) -> bool:
        return self.dama

    def setDama(self, dama: bool):
        self.dama = dama

    def getJogador(self) -> Jogador:
        return self.jogador

    def setJogador(self, jogador: Jogador):
        self.jogador = jogador

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import CorPeca
from typing import List

class Jogador(object):

    def __init__(self):
        self.nome: str = None
        self.daVez: bool = None
        self.vencedor: bool = None
        self.damas: int = 0
        self.peoes: int = 12
        self.pecasEmJogo: int = 12
        self.idJogador: int = None

    def getNome(self) -> str:
        return self.nome

    def setNome(self, nome: str) -> None:
        self.nome = nome

    def getDaVez(self) -> bool:
        return self.daVez

    def setDaVez(self, daVez: bool) -> None:
        self.daVez = daVez

    def getVencedor(self) -> bool:
        return self.vencedor

    def setVencedor(self, vencedor: bool) -> None:
        self.vencedor = vencedor

    def update_pecas(self, cor: CorPeca):
        pass

    def getDamas(self) -> int:
        return self.damas

    def getPeoes(self) -> int:
        return self.peoes

    def diminuirPeoes(self) -> None:
        self.peoes -= 1

    def aumentarDamas(self) -> None:
        self.diminuirPeoes()
        self.damas += 1

    def getPecasEmJogo(self) -> int:
        return self.pecasEmJogo

    def diminuirPecasEmJogo(self, ehPeao: bool) -> None:
        if ehPeao:
            self.diminuirPeoes()
        else:
            self.damas -= 1
        self.pecasEmJogo -= 1

    def setIdJogador(self, idJogador):
        self.idJogador = idJogador

    def getIdJogador(self):
        return self.idJogador

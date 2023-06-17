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
        self.pecasNorm: int = 12
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

    def getNormalPieces(self) -> int:
        pass

    def setIdJogador(self, idJogador):
        self.idJogador = idJogador

    def getIdJogador(self):
        return self.idJogador

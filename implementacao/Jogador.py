#!/usr/bin/python
# -*- coding: UTF-8 -*-
import CorPeca
from typing import List


class Jogador(object):

    def __init__(self):
        self.nome: str = None
        self.pecas: list = None
        self.daVez: bool = None
        self.vencedor: bool = None
        self.damas: int = None
        self.pecasNorm: int = None

    def getNome(self) -> str:
        return self.nome

    def setNome(self, nome: str) -> None:
        self.nome = nome

    def getPecas(self) -> list:
        return self.pecas

    def setPecas(self, peca: list) -> None:
        pass

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

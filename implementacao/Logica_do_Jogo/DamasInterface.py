#!/usr/bin/python
# -*- coding: UTF-8 -*-


class DamasInterface(object):
    def __init__(self):
        self.message: str = None
        self.positions: list = None

    def getMessage(self) -> str:
        return self.message

    def setMessage(self, message: str):
        pass

    def getValue(self, linha: int, coluna: int, empate: bool) -> int:
        pass

    def setValue(self, linha: int, coluna: int, empate: bool):
        pass

    def get_match_status(self) -> int:
        pass

    def set_match_status(self, match_status: int):
        pass

    def getPositions(self):
        pass

    def setPositions(self, positions) -> None:
        pass

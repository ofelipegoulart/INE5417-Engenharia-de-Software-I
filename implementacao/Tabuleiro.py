from implementacao.CorCasa import CorCasa
from implementacao.CorPeca import CorPeca
from implementacao.Jogador import Jogador
from implementacao.Lance import Lance
from implementacao.Logica_do_Jogo.DamasInterface import DamasInterface
from implementacao.Peca import Peca
from implementacao.Position import Position


# from implementacao.Logica_do_Jogo.actorPlayer import ActorPlayer


class Tabuleiro:
    def __init__(self, tk):
        super().__init__()
        self.jogadorLocal = Jogador()
        self.jogadorRemoto = Jogador()
        self.match_id: str = None
        self.match_status: int = 0
        self.positions: list[Position] = []
        self.rodadasSemCaptura: int = 0
        self.pecaClicada: Position = None
        self.proposta_empate: bool = False
        self.jogadas = None
        self.errorLocalMessage = None
        self.pecasCapturadas: list[Peca] = []

    def click(self, linha: int, coluna: int, local_turn: bool):
        state = self.getEstado()
        proposta_empate = self.get_proposta_empate()
        # Verifica se há uma proposta de empate
        if not proposta_empate:
            # Verifica se o clique foi em linha em colu na ao invés de oferecer empate
            if linha is not None and coluna is not None:
                # Verifica se é a vez do jogador
                if local_turn:
                    # Pega a posicao que foi clicada
                    positionClicada = self.getPositionByLinhaColuna(
                        linha, coluna)
                    # Verifica se existe uma peca já selecionada
                    if self.pecaClicada is None:
                        casaEhValida = self.verificarCasa(positionClicada)
                        if casaEhValida:
                            # Muda valor de peça selecionada
                            jogadas = self.verificarPossiveisCasas(
                                positionClicada)  # TODO: Precisa receber uma peca
                            self.jogadas = jogadas
                            self.setPecaClicada(positionClicada)
                            return False
                            # TODO: Talvez, ao invés de um booleano, essa flag poderia ser o objeto Peca
                        elif not casaEhValida:
                            self.errorLocalMessage = "Casa inválida para jogada"
                            return False
                    # Caso não haja, ele tenta validar a jogada
                    elif self.pecaClicada is not None:
                        # if()
                        for position in self.jogadas:
                            if position.coluna == positionClicada.coluna and position.linha == positionClicada.linha:
                                return True
                        self.pecaClicada = None
                        self.errorLocalMessage = "Casa inválida para jogada (segundo clique)"
                        return False

                        # if not jogadas:
                        #     # Se jogadas estiver vazia, jogada Inválida
                        #     pass
                        # else:
                        #     for jogada in jogadas:
                        #         if positionClicada.linha == jogada.linha and positionClicada.coluna == jogada.coluna:
                        #             return  # Jogada válida
                elif not local_turn:
                    self.errorLocalMessage = "Não é seu turno"
                    return False
            elif linha is None and coluna is None:
                return False

    def verificarPossiveisCasas(self, position: Position) -> list[Position]:
        jogadas: list[Position] = []
        linha = position.linha
        coluna = position.coluna
        peca = position.getOcupante()
        if peca.cor == CorPeca.PRETO:
            direcao = 1
        else:
            direcao = -1

        # Verificar movimento na diagonal esquerda
        if coluna > 0:
            nova_linha = linha + direcao
            nova_coluna_esquerda = coluna - 1
            nova_coluna_direita = coluna + 1
            # Testa pra ver se saiu do limite
            # Testa pra ver se a casa da esquerda não tem ocupante
            if self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda).ocupante is None and self.getPositionByLinhaColuna(nova_linha, nova_coluna_direita).ocupante is None:
                jogadas.append(self.getPositionByLinhaColuna(
                    nova_linha, nova_coluna_direita))
                jogadas.append(self.getPositionByLinhaColuna(
                    nova_linha, nova_coluna_esquerda))
            else:
                while self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda).ocupante is not None or self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda).ocupante is not None:
                    if self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda).ocupante is not None and self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda).getOcupante().getJogador() == self.jogadorLocal:
                        jogadas.append(self.getPositionByLinhaColuna(
                            nova_linha + direcao, nova_coluna_esquerda - 1))
                        self.pecasCapturadas.append(self.getPositionByLinhaColuna(
                            nova_linha, nova_coluna_esquerda).getOcupante())
                        nova_coluna_esquerda -= 1
                    if self.getPositionByLinhaColuna(nova_linha, nova_coluna_direita).ocupante is not None and self.getPositionByLinhaColuna(nova_linha, nova_coluna_direita).getOcupante().getJogador() == self.jogadorLocal:
                        jogadas.append(self.getPositionByLinhaColuna(
                            nova_linha + direcao, nova_coluna_direita + 1))
                        self.pecasCapturadas.append(self.getPositionByLinhaColuna(
                            nova_linha, nova_coluna_direita).getOcupante())
                        nova_coluna_direita += 1
            return jogadas

            # Testa pra ver se a casa da direita não tem ocupante
            # if self.getPositionByLinhaColuna(nova_linha, nova_coluna_direta).ocupante is None:
            # Pode jogar pros dois lados
            # jogadas.append(self.getPositionByLinhaColuna(nova_linha, nova_coluna_direta))
            # jogadas.append(self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda))
            # possivelJogada pra esquerda
            # existe ocupante na posição final quando eu comer a peça
            # se nao testar se na posição final da jogada ainda existe possiblidade de comer mais damas (enquanto puder, eu preciso continuar checando)
            # Essa função de checagem precisa saber se a peça a ser mexida é dama ou não (se ela for, precisa checar nas duas diagonais)

        # Possibilita a dama ir para a outra direcao
        if peca.dama:
            direcao = direcao * -1

            # Verificar movimento na diagonal esquerda
            if coluna > 0:
                nova_linha = linha + direcao
                nova_coluna = coluna - 1
                if self.getPositionByLinhaColuna(nova_linha, nova_coluna).ocupante is None:
                    # TODO: Talvez precise verificar se está fora do tabuleiro
                    jogadas.append(self.getPositionByLinhaColuna(
                        nova_linha, nova_coluna))

            # Verificar movimento na diagonal direita
            if coluna <= 7:
                nova_linha = linha + direcao
                nova_coluna = coluna - 1
                if self.getPositionByLinhaColuna(nova_linha, nova_coluna).ocupante is None:
                    # TODO: Talvez precise verificar se está fora do tabuleiro
                    jogadas.append(self.getPositionByLinhaColuna(
                        nova_linha, nova_coluna))

        return jogadas

    # def getCapturasMultiplas(self, linha, coluna):

    def getPositionByLinhaColuna(self, linha: int, coluna: int) -> Position:
        for position in self.positions:
            if position.linha == linha and position.coluna == coluna:
                return position

    def verificarCasa(self, position: Position):
        if position.casa == CorCasa.PRETO:
            # Verifica se a casa selecionada tem uma peça do usuário

            peca1 = self.getPositionByLinhaColuna(
                position.linha, position.coluna).getOcupante()
            if peca1 is not None:
                peca = position.ocupante
                if peca.jogador == self.jogadorLocal:
                    # Verifica se a peça que está na casa não está bloqueada
                    if not self.pecaBloqueada(position):
                        return True
            else:
                return False

    def pecaBloqueada(self, position: Position):
        i = position.linha - 1
        j = position.coluna - 1
        if i >= 0 and j >= 0:
            if self.getPositionByLinhaColuna(i, j).ocupante is None:
                return False
            elif i - 1 >= 0 and j - 1 >= 0:
                if self.getPositionByLinhaColuna(i - 1, j - 1).ocupante is None:
                    return False
        else:
            i = position.linha - 1
            j = position.coluna + 1
            if i >= 0 and j >= 0:
                if self.getPositionByLinhaColuna(i, j).ocupante is None:
                    return False
                elif i - 1 >= 0 and j - 1 >= 0:
                    if self.getPositionByLinhaColuna(i - 1, j - 1).ocupante is None:
                        return False
            else:
                return True

        # if state == 3 or state == 2:
        #     if self.pecaClicada:
        #         lance = Lance(linha, coluna)
        #         self.fazerLance(lance)
        #     else:
        #         self.pecaClicada = True
        # else:
        #     return

    def getPlayers(self) -> list[Jogador]:
        lisPlayers = []
        lisPlayers.append(self.jogadorLocal)
        lisPlayers.append(self.jogadorRemoto)
        return lisPlayers

    def getJogadas(self) -> list[Position]:
        return self.jogadas

    def iniciarPartida(self, local_turn: bool):
        pass

    def fazerLance(self, lance: Lance):
        pass

    def reiniciar(self):
        pass

    def getEstado(self) -> DamasInterface:
        pass

    def setStatus(self, status: int):
        pass

    def getPosicao(self, lance: Lance) -> Position:
        pass

    def getJogadorConectado(self) -> Jogador:
        pass

    def getJogadorDesconectado(self) -> Jogador:
        pass

    def assumirVencedor(self, lance: Lance):
        pass

    def getStatus(self) -> int:
        pass

    def getPositions(self) -> list[Position]:
        return self.positions

    def setPositions(self, positions: list[Position]):
        self.positions = positions

    def evaluateEndGame(self, lance: Lance) -> bool:
        pass

    def getRodadasSemCaptura(self) -> int:
        return self.rodadasSemCaptura

    def appendRodadasSemCaptura(self) -> None:
        pass

    def zerarRodadasSemCaptura(self) -> None:
        pass

    def getPecaClicada(self) -> Position:
        return self.pecaClicada

    def setPecaClicada(self, pecaClicada: Position):
        self.pecaClicada = pecaClicada

    def set_proposta_empate(self, proposta_empate: bool):
        self.proposta_empate = proposta_empate

    def get_proposta_empate(self):
        return self.proposta_empate

    def getPecasCapturadas(self):
        return self.pecasCapturadas

    def trocarTurnos(self):
        if self.jogadorLocal.daVez:
            self.jogadorRemoto.daVez = True
            self.jogadorLocal.daVez = False
        else:
            self.jogadorLocal.daVez = True
            self.jogadorRemoto.daVez = False

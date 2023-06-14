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
        self.jogadorLocal = None
        self.jogadorRemoto = None
        self.match_id: str = None
        self.match_status: int = 0
        self.positions: list = []
        self.rodadasSemCaptura: int = 0
        self.pecaClicada: Peca = None
        self.proposta_empate: bool = False

    def click(self, linha: int, coluna: int, local_turn: bool):
        state = self.getEstado()
        proposta_empate = self.get_proposta_empate()
        # Verifica se há uma proposta de empate
        if not proposta_empate:
            if linha and coluna is not None:
                # Verifica se é a vez do jogador
                if local_turn:
                    # Pega a posicao que foi clicada
                    positionClicada = self.getPositionByLinhaColuna(linha, coluna)
                    # Verifica se existe uma peca já selecionada
                    if self.pecaClicada is None:
                        if self.verificarCasa(positionClicada):
                            self.setPecaClicada(positionClicada.ocupante)
                            # TODO: Talvez, ao invés de um booleano, essa flag poderia ser o objeto Peca
                    # Caso não haja, ele tenta validar a jogada
                    else:
                        jogadas = self.verificarPossiveisCasas(
                            positionClicada.ocupante)  # TODO: Precisa receber uma peca

                        if not jogadas:
                            # Se jogadas estiver vazia, jogada Inválida
                            pass
                        else:
                            for jogada in jogadas:
                                if positionClicada.linha == jogada.linha and positionClicada.coluna == jogada.coluna:
                                    return  # Jogada válida

    def verificarPossiveisCasas(self, peca: Peca):
        jogadas: list[Position] = []
        linha = peca.casa.linha
        coluna = peca.casa.coluna
        if peca.cor == CorPeca.PRETO:
            direcao = -1
        else:
            direcao = 1

        # Verificar movimento na diagonal esquerda
        if coluna > 0:
            nova_linha = linha + direcao
            nova_coluna = coluna - 1
            if self.getPositionByLinhaColuna(nova_linha, nova_coluna).ocupante is None:
                # TODO: Talvez precise verificar se está fora do tabuleiro
                jogadas.append(self.getPositionByLinhaColuna(nova_linha, nova_coluna))

        # Verificar movimento na diagonal direita
        if coluna <= 7:
            nova_linha = linha + direcao
            nova_coluna = coluna - 1
            if self.getPositionByLinhaColuna(nova_linha, nova_coluna).ocupante is None:
                # TODO: Talvez precise verificar se está fora do tabuleiro
                jogadas.append(self.getPositionByLinhaColuna(nova_linha, nova_coluna))

        # Possibilita a dama ir para a outra direcao
        if peca.dama:
            direcao = direcao * -1

            # Verificar movimento na diagonal esquerda
            if coluna > 0:
                nova_linha = linha + direcao
                nova_coluna = coluna - 1
                if self.getPositionByLinhaColuna(nova_linha, nova_coluna).ocupante is None:
                    ##TODO: Talvez precise verificar se está fora do tabuleiro
                    jogadas.append(self.getPositionByLinhaColuna(nova_linha, nova_coluna))

            # Verificar movimento na diagonal direita
            if coluna <= 7:
                nova_linha = linha + direcao
                nova_coluna = coluna - 1
                if self.getPositionByLinhaColuna(nova_linha, nova_coluna).ocupante is None:
                    ##TODO: Talvez precise verificar se está fora do tabuleiro
                    jogadas.append(self.getPositionByLinhaColuna(nova_linha, nova_coluna))

        return jogadas

    def getPositionByLinhaColuna(self, linha: int, coluna: int) -> Position:
        for position in self.positions:
            if position.linha == linha and position.coluna == coluna:
                return position

    def verificarCasa(self, position: Position):
        if position.casa == CorCasa.PRETO:
            peca = position.informarOcupante(position.linha, position.coluna)
            if peca.jogador == self.jogadorLocal:
                if not self.pecaBloqueada(peca):
                    return True

    def pecaBloqueada(self, peca: Peca):
        i = peca.casa.linha - 1
        j = peca.casa.coluna - 1
        if i >= 0 and j >= 0:
            if self.getPositionByLinhaColuna(i, j).ocupante is None:
                return False
            elif i - 1 >= 0 and j - 1 >= 0:
                if self.getPositionByLinhaColuna(i - 1, j - 1).ocupante is None:
                    return False
        else:
            i = peca.casa.linha - 1
            j = peca.casa.coluna + 1
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

    def getPositions(self) -> Position:
        pass

    def setPositions(self, position):
        pass

    def evaluateEndGame(self, lance: Lance) -> bool:
        pass

    def getRodadasSemCaptura(self) -> int:
        return self.rodadasSemCaptura

    def appendRodadasSemCaptura(self) -> None:
        pass

    def zerarRodadasSemCaptura(self) -> None:
        pass

    def getPecaClicada(self):
        return self.pecaClicada

    def setPecaClicada(self, pecaClicada: Peca):
        self.pecaClicada = pecaClicada

    def set_proposta_empate(self, proposta_empate: bool):
        self.proposta_empate = proposta_empate

    def get_proposta_empate(self):
        return self.proposta_empate

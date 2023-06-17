from implementacao.CorCasa import CorCasa
from implementacao.CorPeca import CorPeca
from implementacao.Jogador import Jogador
from implementacao.Lance import Lance
from implementacao.Logica_do_Jogo.DamasInterface import DamasInterface
from implementacao.MatchStatus import MatchStatus
from implementacao.Peca import Peca
from implementacao.Position import Position


class Tabuleiro:
    def __init__(self, tk):
        super().__init__()
        self.jogadorLocal = Jogador()
        self.jogadorRemoto = Jogador()
        self.match_id: str = None
        # 0 - em andamento, 1 - empate, 2 - vitoria/encerrada
        self.match_status: MatchStatus = MatchStatus.EM_ANDAMENTO
        self.positions: list[Position] = []
        self.rodadasSemCaptura: int = 0
        self.pecaClicada: Position = None
        self.proposta_empate: bool = False
        self.jogadas: list[Position] = []
        self.errorLocalMessage = None
        self.pecasCapturadas: list[Peca] = []
        self.lances: list[Lance] = []

    def click(self, linha: int, coluna: int, local_turn: bool) -> bool:
        state = self.getEstado()
        proposta_empate = self.get_proposta_empate()

        # Verifica se há uma proposta de empate
        if not proposta_empate:
            # Verifica se o clique foi em linha e coluna ao invés de oferecer empate
            if linha is not None and coluna is not None:
                # Verifica se é a vez do jogador
                if local_turn:
                    # Pega a posição que foi clicada
                    positionClicada = self.getPositionByLinhaColuna(
                        linha, coluna)

                    # Verifica se existe uma peça já selecionada
                    if self.pecaClicada is None:
                        casaEhValida = self.verificarCasa(positionClicada)
                        if casaEhValida:
                            jogadas = self.verificarPossiveisCasas(
                                positionClicada)
                            self.jogadas = jogadas
                            self.setPecaClicada(positionClicada)
                            return False
                        elif not casaEhValida:
                            self.errorLocalMessage = "Casa inválida para jogada"
                            return False

                    # Caso já haja, ele tenta validar a jogada
                    elif self.pecaClicada is not None:
                        for position in self.jogadas:
                            if position.coluna == positionClicada.coluna and position.linha == positionClicada.linha:
                                return True
                        self.pecaClicada = None
                        self.errorLocalMessage = "Casa inválida para jogada (segundo clique)"
                        return False

                elif not local_turn:
                    self.errorLocalMessage = "Não é seu turno"
                    return False

            elif linha is None and coluna is None:
                return False

    def verificarPossiveisCasas(self, position: Position):
        possiveis_casas = []

        if position.ocupante is None:  # Verifica se a posição está vazia
            return possiveis_casas

        peca = position.ocupante
        linha = position.linha
        coluna = position.coluna

        if peca.dama:
            possiveis_casas += self.verificarMovimentosDama(position)
        else:
            possiveis_casas += self.verificarMovimentosPeao(position)

        return possiveis_casas

    def verificarMovimentosPeao(self, position: Position):
        possiveis_casas = []
        peca = position.ocupante
        linha = position.getLinha()
        coluna = position.getColuna()
        cor = peca.getCor()

        # Define as direções de movimento para o peão com base na cor
        direcao = 0

        if cor == CorPeca.PRETO:
            direcao = 1  # Movimento para baixo
        else:  # CorPeca.VERMELHO
            direcao = -1  # Movimento para cima

        # Verifica movimento para frente
        nova_linha = linha + direcao
        nova_coluna_esquerda = coluna - 1
        nova_coluna_direita = coluna + 1

        if 0 <= nova_linha <= 7 and 0 <= nova_coluna_esquerda <= 7:
            if self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda).ocupante is None:
                possiveis_casas.append(self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda))

        if 0 <= nova_linha <= 7 and 0 <= nova_coluna_direita <= 7:
            if self.getPositionByLinhaColuna(nova_linha, nova_coluna_direita).ocupante is None:
                possiveis_casas.append(self.getPositionByLinhaColuna(nova_linha, nova_coluna_direita))

        # Verifica movimento para captura
        nova_linha = linha + (direcao * 2)
        nova_coluna_esquerda = coluna - 2
        nova_coluna_direita = coluna + 2

        while True:
            capturou = False

            if 0 <= nova_linha <= 7 and 0 <= nova_coluna_esquerda <= 7:
                peca_inimiga = self.getPositionByLinhaColuna(linha + direcao, coluna - 1).ocupante
                peca_vazia = self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda).ocupante

                if peca_inimiga is not None and peca_vazia is None and peca_inimiga.getCor() != cor:
                    # self.pecasCapturadas.append(peca_inimiga)
                    proxima_casa = self.getPositionByLinhaColuna(nova_linha, nova_coluna_esquerda)
                    possiveis_casas.append(proxima_casa)
                    capturou = True

                    # Verifica capturas múltiplas na diagonal esquerda
                    proxima_linha = nova_linha + direcao
                    proxima_coluna = nova_coluna_esquerda - 1
                    proxima_casa = self.getPositionByLinhaColuna(proxima_linha, proxima_coluna)
                    # if proxima_casa.getOcupante() is not None and proxima_casa.getOcupante().getCor() != cor and \
                    #         self.pecaIsCapturable(position, proxima_casa, direcao=direcao):
                    #     self.pecasCapturadas.append(peca_inimiga)

            if 0 <= nova_linha <= 7 and 0 <= nova_coluna_direita <= 7:
                peca_inimiga = self.getPositionByLinhaColuna(linha + direcao, coluna + 1).ocupante
                peca_vazia = self.getPositionByLinhaColuna(nova_linha, nova_coluna_direita).ocupante

                if peca_inimiga is not None and peca_vazia is None and peca_inimiga.getCor() != cor:
                    # self.pecasCapturadas.append(peca_inimiga)
                    proxima_casa = self.getPositionByLinhaColuna(nova_linha, nova_coluna_direita)
                    possiveis_casas.append(proxima_casa)
                    capturou = True

                    # Verifica capturas múltiplas na diagonal direita
                    proxima_linha = nova_linha + direcao
                    proxima_coluna = nova_coluna_direita + 1
                    proxima_casa = self.getPositionByLinhaColuna(proxima_linha, proxima_coluna)
                    # if proxima_casa.getOcupante() is not None and proxima_casa.getOcupante().getCor() != cor and \
                    #         self.pecaIsCapturable(position, proxima_casa, direcao=direcao):
                    #     self.pecasCapturadas.append(peca_inimiga)

            if not capturou:
                break

            nova_linha += (direcao * 2)
            nova_coluna_esquerda -= 2
            nova_coluna_direita += 2

        return possiveis_casas


    def verificarMovimentosDama(self, position: Position):
        possiveis_casas = []
        peca = position.ocupante
        linha = position.linha
        coluna = position.coluna
        cor = peca.getCor()

        # Verifica movimentos nas quatro direções (diagonais)
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direcao in direcoes:
            delta_linha, delta_coluna = direcao
            nova_linha = linha + delta_linha
            nova_coluna = coluna + delta_coluna

            while 0 <= nova_linha <= 7 and 0 <= nova_coluna <= 7:
                nova_posicao = self.getPositionByLinhaColuna(nova_linha, nova_coluna)

                if nova_posicao.ocupante is None:
                    possiveis_casas.append(nova_posicao)
                else:
                    if nova_posicao.ocupante.getCor() != cor:
                        if 0 <= nova_linha + delta_linha <= 7 and 0 <= nova_coluna + delta_coluna <= 7:
                            proxima_posicao = self.getPositionByLinhaColuna(nova_linha + delta_linha,
                                                                            nova_coluna + delta_coluna)
                            if proxima_posicao.ocupante is None:
                                possiveis_casas.append(proxima_posicao)

                nova_linha += delta_linha
                nova_coluna += delta_coluna

        return possiveis_casas

    def pecaIsCapturable(self, posicaoPlayer: Position, posicaoAdversario: Position, direcao):
        # Verifica se esta na diagonal esquerda
        if posicaoPlayer.getColuna() == posicaoAdversario.getColuna() + direcao and posicaoPlayer.getLinha() == posicaoAdversario.getLinha() + direcao:
            if self.getPositionByLinhaColuna(posicaoAdversario.getLinha() + (direcao * 2),
                                             posicaoAdversario.getColuna() + (direcao * 2)).getOcupante() is not None:
                return True
        else:
            return False

    def verificaCapturas(self, positionInicial: Position, positionFinal: Position, cor: CorPeca):
        direcao = 1 if cor == CorPeca.PRETO else -1
        linha_inicial = positionInicial.getLinha()
        linha_final = positionFinal.getLinha()
        coluna_inicial = positionInicial.getColuna()
        coluna_final = positionFinal.getColuna()

        if linha_final > linha_inicial and coluna_final > coluna_inicial:
            # Movimento diagonal para a direita e para baixo
            for i in range(linha_inicial + 1, linha_final):
                j = coluna_inicial + (i - linha_inicial)
                ocupante = self.getPositionByLinhaColuna(i, j).getOcupante()
                if ocupante is not None and ocupante.getCor() != cor:
                    self.pecasCapturadas.append(ocupante)

        elif linha_final > linha_inicial and coluna_final < coluna_inicial:
            # Movimento diagonal para a esquerda e para baixo
            for i in range(linha_inicial + 1, linha_final):
                j = coluna_inicial - (i - linha_inicial)
                ocupante = self.getPositionByLinhaColuna(i, j).getOcupante()
                if ocupante is not None and ocupante.getCor() != cor:
                    self.pecasCapturadas.append(ocupante)

        elif linha_final < linha_inicial and coluna_final > coluna_inicial:
            # Movimento diagonal para a direita e para cima
            for i in range(linha_inicial - 1, linha_final, -1):
                j = coluna_inicial + (linha_inicial - i)
                ocupante = self.getPositionByLinhaColuna(i, j).getOcupante()
                if ocupante is not None and ocupante.getCor() != cor:
                    self.pecasCapturadas.append(ocupante)

        elif linha_final < linha_inicial and coluna_final < coluna_inicial:
            # Movimento diagonal para a esquerda e para cima
            for i in range(linha_inicial - 1, linha_final, -1):
                j = coluna_inicial - (linha_inicial - i)
                ocupante = self.getPositionByLinhaColuna(i, j).getOcupante()
                if ocupante is not None and ocupante.getCor() != cor:
                    self.pecasCapturadas.append(ocupante)

    def getPositionByLinhaColuna(self, linha: int, coluna: int) -> Position:
        for position in self.positions:
            if position.linha == linha and position.coluna == coluna:
                return position

    def verificarCasa(self, position: Position) -> bool:
        if position.casa == CorCasa.PRETO:
            peca1 = self.getPositionByLinhaColuna(
                position.linha, position.coluna).getOcupante()
            if peca1 is not None:
                peca = position.ocupante
                if peca.jogador == self.jogadorLocal:
                    if not self.pecaBloqueada(position):
                        return True
            else:
                return False

    def pecaBloqueada(self, position: Position) -> bool:
        # TODO: precisa fazer esse método funcionar

        # linha = position.getLinha()
        # coluna = position.getColuna()
        # peca = position.getOcupante()
        # cor = peca.getCor()

        # # Verifica se há peças da mesma cor ao redor da posição
        # for i in [-1, 1]:
        #     for j in [-1, 1]:
        #         nova_linha = linha + i
        #         nova_coluna = coluna + j

        #         if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
        #             posicao_vizinha = self.getPositionByLinhaColuna(nova_linha, nova_coluna)
        #             peca_vizinha = posicao_vizinha.getOcupante()

        #             if peca_vizinha is not None and peca_vizinha.getCor() == cor:
        #                 return True

        # # Verifica peças nas colunas iniciais e finais
        # if coluna == 0 or coluna == 7:
        #     nova_linha = linha + 1 if cor == CorPeca.PRETO else linha - 1

        #     if 0 <= nova_linha < 8:
        #         posicao_esquerda = self.getPositionByLinhaColuna(nova_linha, coluna - 1)
        #         posicao_direita = self.getPositionByLinhaColuna(nova_linha, coluna + 1)

        #         if coluna == 0:
        #             peca_esquerda = posicao_esquerda.getOcupante()
        #             if peca_esquerda is not None and peca_esquerda.getCor() == cor:
        #                 return True

        #         if coluna == 7:
        #             peca_direita = posicao_direita.getOcupante()
        #             if peca_direita is not None and peca_direita.getCor() == cor:
        #                 return True

        # # Verifica peças nas linhas iniciais e finais
        # if linha == 0 or linha == 7:
        #     if linha == 0:
        #         posicao_abaixo_esquerda = self.getPositionByLinhaColuna(linha + 1, coluna - 1)
        #         posicao_abaixo_direita = self.getPositionByLinhaColuna(linha + 1, coluna + 1)

        #         peca_abaixo_esquerda = posicao_abaixo_esquerda.getOcupante()
        #         peca_abaixo_direita = posicao_abaixo_direita.getOcupante()

        #         if peca_abaixo_esquerda is not None and peca_abaixo_esquerda.getCor() == cor:
        #             return True

        #         if peca_abaixo_direita is not None and peca_abaixo_direita.getCor() == cor:
        #             return True

        #     if linha == 7:
        #         posicao_acima_esquerda = self.getPositionByLinhaColuna(linha - 1, coluna - 1)
        #         posicao_acima_direita = self.getPositionByLinhaColuna(linha - 1, coluna + 1)

        #         peca_acima_esquerda = posicao_acima_esquerda.getOcupante()
        #         peca_acima_direita = posicao_acima_direita.getOcupante()

        #         if peca_acima_esquerda is not None and peca_acima_esquerda.getCor() == cor:
        #             return True

        #         if peca_acima_direita is not None and peca_acima_direita.getCor() == cor:
        #             return True

        # return False
        return False

    def getPlayers(self) -> list[Jogador]:
        lisPlayers = []
        lisPlayers.append(self.jogadorLocal)
        lisPlayers.append(self.jogadorRemoto)
        return lisPlayers

    def avaliarEncerramento(self):
        for jogador in self.getPlayers():
            if not jogador.daVez:
                if len(self.getPositionsWithPiecesOfPlayer(jogador)) == 0:
                    self.setStatus(MatchStatus.VENCEDOR)
                    return True
                else:
                    pecasBloqueadas: list[Peca] = []
                    for position in self.getPositionsWithPiecesOfPlayer(jogador):
                        if self.pecaBloqueada(position=position):
                            pecasBloqueadas.append(position.getOcupante())
                    if len(pecasBloqueadas) == len(self.getPlayerPieces(jogador)):
                        self.setStatus(MatchStatus.VENCEDOR)
                        return True
                    else:
                        if len(self.lances) >= 20:
                            lancesDama: list[Lance] = []
                            for lance in self.getLances():
                                if lance.getPeca().getDama():
                                    lancesDama.append(lance)
                            if len(lancesDama) == 20:
                                self.setStatus(MatchStatus.EMPATE)
                                return True
                            else:
                                empate = self.verificarEmpate()
                                if (empate):
                                    self.setStatus(MatchStatus.EMPATE)
                                    return True
                                else:
                                    return False

    def verificarEmpate(self):
        lancesSemCaptura: list[Lance] = []
        for lance in self.lances:
            if not lance.getCaptura():
                lancesSemCaptura.append(lance)
        if len(lancesSemCaptura) == 5:
            pecasLocal: list[Peca] = self.getPlayerPieces(self.jogadorLocal)
            pecasRemoto: list[Peca] = self.getPlayerPieces(self.jogadorRemoto)
            if len(pecasLocal) == 2 and len(pecasRemoto) == 2:
                damasLocal: list[Peca] = []
                for pecaLocal in pecasLocal:
                    if pecaLocal.getDama():
                        damasLocal.append(pecaLocal)
                damasRemoto: list[Peca] = []
                for pecaRemoto in pecasRemoto:
                    if pecaRemoto.getDama():
                        damasRemoto.append(pecaRemoto)
                if len(damasLocal) == 2 and len(damasRemoto) == 2:
                    return True
                if (len(damasLocal) == 2 and len(damasRemoto) == 1) or (len(damasLocal) == 1 and len(damasRemoto) == 2):
                    return True
        else:
            return False

    def removerPecas(self):
        for position in self.getPositions():
            for peca in self.pecasCapturadas:
                if position.getOcupante() is not None and peca is not None and peca.getId() == position.getOcupante().getId():
                    position.setOcupante(None)

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
        self.match_status = status

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

    def getPositionsWithPiecesOfPlayer(self, jogador: Jogador) -> list[Position]:
        finalList: list[Position] = []
        for position in self.getPositions():
            if position.getOcupante() == jogador:
                finalList.append(position)
        return finalList

    def getPlayerPieces(self, jogador: Jogador) -> list[Peca]:
        finalList: list[Peca] = []
        for position in self.getPositions():
            if position.getOcupante() == jogador:
                finalList.append(position.getOcupante())
        return finalList

    def trocarTurnos(self):
        if self.jogadorLocal.daVez:
            self.jogadorRemoto.daVez = True
            self.jogadorLocal.daVez = False
        else:
            self.jogadorLocal.daVez = True
            self.jogadorRemoto.daVez = False

    def getLances(self) -> list[Lance]:
        return self.lances

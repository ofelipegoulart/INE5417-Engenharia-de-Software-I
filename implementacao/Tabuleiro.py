from implementacao.CorCasa import CorCasa
from implementacao.CorPeca import CorPeca
from implementacao.Jogador import Jogador
from implementacao.Lance import Lance
from implementacao.Logica_do_Jogo.DamasInterface import DamasInterface
from implementacao.MatchStatus import MatchStatus
from implementacao.Peca import Peca
from implementacao.Position import Position
from implementacao.StatusPropostaEmpate import StatusPropostaEmpate


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
        self.perdedor: Jogador = None
        self.statusPropostaEmpate: StatusPropostaEmpate = StatusPropostaEmpate.SEM_PROPOSTA

    def click(self, linha: int, coluna: int, local_turn: bool, aceitaPropostaEmpate: bool or None) -> bool:
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
            elif coluna is None and linha is None:
                self.set_proposta_empate(True)
                self.statusPropostaEmpate = StatusPropostaEmpate.LOCAL_ENVIOU
                return True
        elif self.get_proposta_empate():
            if aceitaPropostaEmpate:
                self.statusPropostaEmpate = StatusPropostaEmpate.LOCAL_ACEITOU
                return True
            elif not aceitaPropostaEmpate:
                self.statusPropostaEmpate = StatusPropostaEmpate.SEM_PROPOSTA
                return True

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
        nova_linha_casa_vazia = linha + direcao
        nova_coluna_esquerda_casa_vazia = coluna - 1
        nova_coluna_direita_casa_vazia = coluna + 1

        if 0 <= nova_linha_casa_vazia <= 7 and 0 <= nova_coluna_esquerda_casa_vazia <= 7:
            if self.getPositionByLinhaColuna(nova_linha_casa_vazia, nova_coluna_esquerda_casa_vazia).ocupante is None:
                possiveis_casas.append(
                    self.getPositionByLinhaColuna(nova_linha_casa_vazia, nova_coluna_esquerda_casa_vazia))

        if 0 <= nova_linha_casa_vazia <= 7 and 0 <= nova_coluna_direita_casa_vazia <= 7:
            if self.getPositionByLinhaColuna(nova_linha_casa_vazia, nova_coluna_direita_casa_vazia).ocupante is None:
                possiveis_casas.append(
                    self.getPositionByLinhaColuna(nova_linha_casa_vazia, nova_coluna_direita_casa_vazia))

        # Verifica movimento para captura
        nova_linha_casa_vazia = linha + (direcao * 2)
        nova_coluna_esquerda_casa_vazia = coluna - 2
        nova_coluna_direita_casa_vazia = coluna + 2

        linha_peca_alvo = linha + direcao
        coluna_esquerda_peca_alvo = coluna - 1
        coluna_direita_peca_alvo = coluna + 1

        while True:
            capturou = False

            if 0 <= nova_linha_casa_vazia <= 7 and 0 <= nova_coluna_esquerda_casa_vazia <= 7:
                # Verifica se há uma peça inimiga na diagonal esquerda
                peca_inimiga = self.getPositionByLinhaColuna(linha_peca_alvo, coluna_esquerda_peca_alvo).ocupante
                # Verifica se a casa atras da peça inimiga está vazia
                casa_vazia = self.getPositionByLinhaColuna(nova_linha_casa_vazia,
                                                           nova_coluna_esquerda_casa_vazia).ocupante

                # Se há peça inimiga na diagonal esquerda e a peça atras
                if peca_inimiga is not None and casa_vazia is None and peca_inimiga.getCor() != cor:
                    # self.pecasCapturadas.append(peca_inimiga)
                    proxima_casa = self.getPositionByLinhaColuna(nova_linha_casa_vazia, nova_coluna_esquerda_casa_vazia)
                    possiveis_casas.append(proxima_casa)
                    capturou = True

            if 0 <= nova_linha_casa_vazia <= 7 and 0 <= nova_coluna_direita_casa_vazia <= 7:
                peca_inimiga = self.getPositionByLinhaColuna(linha_peca_alvo, coluna_direita_peca_alvo).ocupante
                casa_vazia = self.getPositionByLinhaColuna(nova_linha_casa_vazia,
                                                           nova_coluna_direita_casa_vazia).ocupante

                if peca_inimiga is not None and casa_vazia is None and peca_inimiga.getCor() != cor:
                    # self.pecasCapturadas.append(peca_inimiga)
                    proxima_casa = self.getPositionByLinhaColuna(nova_linha_casa_vazia, nova_coluna_direita_casa_vazia)
                    possiveis_casas.append(proxima_casa)
                    capturou = True

            if not capturou:
                break

            nova_linha_casa_vazia += (direcao * 2)
            nova_coluna_esquerda_casa_vazia -= 2
            nova_coluna_direita_casa_vazia += 2
            linha_peca_alvo += (direcao * 2)
            coluna_esquerda_peca_alvo -= 2
            coluna_direita_peca_alvo += 2

        return possiveis_casas

    def verificarMovimentosDama(self, position: Position):
        possiveis_casas = []
        peca = position.ocupante
        linha = position.getLinha()
        coluna = position.getColuna()
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
                        proxima_linha = nova_linha + delta_linha
                        proxima_coluna = nova_coluna + delta_coluna
                        encontrou_captura = False

                        while 0 <= proxima_linha <= 7 and 0 <= proxima_coluna <= 7:
                            proxima_posicao = self.getPositionByLinhaColuna(proxima_linha, proxima_coluna)

                            if proxima_posicao.ocupante is None:
                                # Possível captura múltipla
                                possiveis_casas.append(proxima_posicao)
                                proxima_linha += delta_linha
                                proxima_coluna += delta_coluna
                            else:
                                if encontrou_captura:
                                    break
                                if proxima_posicao.ocupante.getCor() != cor:
                                    encontrou_captura = True

                            nova_linha = proxima_linha
                            nova_coluna = proxima_coluna
                            proxima_linha += delta_linha
                            proxima_coluna += delta_coluna

                nova_linha += delta_linha
                nova_coluna += delta_coluna

        return possiveis_casas

    def verificaCapturas(self, positionInicial: Position, positionFinal: Position, cor: CorPeca):
        direcao = 1 if cor == CorPeca.PRETO else -1
        linha_inicial = positionInicial.getLinha()
        linha_final = positionFinal.getLinha()
        coluna_inicial = positionInicial.getColuna()
        coluna_final = positionFinal.getColuna()
        pecasCapturadasNaRodada: list[Peca] = []

        if linha_final > linha_inicial and coluna_final > coluna_inicial:
            # Movimento diagonal para a direita e para baixo
            for i in range(linha_inicial + 1, linha_final):
                j = coluna_inicial + (i - linha_inicial)
                ocupante = self.getPositionByLinhaColuna(i, j).getOcupante()
                if ocupante is not None and ocupante.getCor() != cor:
                    self.pecasCapturadas.append(ocupante)
                    pecasCapturadasNaRodada.append(ocupante)
                    # self.zerarRodadasSemCaptura()

        elif linha_final > linha_inicial and coluna_final < coluna_inicial:
            # Movimento diagonal para a esquerda e para baixo
            for i in range(linha_inicial + 1, linha_final):
                j = coluna_inicial - (i - linha_inicial)
                ocupante = self.getPositionByLinhaColuna(i, j).getOcupante()
                if ocupante is not None and ocupante.getCor() != cor:
                    self.pecasCapturadas.append(ocupante)
                    pecasCapturadasNaRodada.append(ocupante)
                    # self.zerarRodadasSemCaptura()

        elif linha_final < linha_inicial and coluna_final > coluna_inicial:
            # Movimento diagonal para a direita e para cima
            for i in range(linha_inicial - 1, linha_final, -1):
                j = coluna_inicial + (linha_inicial - i)
                ocupante = self.getPositionByLinhaColuna(i, j).getOcupante()
                if ocupante is not None and ocupante.getCor() != cor:
                    self.pecasCapturadas.append(ocupante)
                    pecasCapturadasNaRodada.append(ocupante)
                    # self.zerarRodadasSemCaptura()

        elif linha_final < linha_inicial and coluna_final < coluna_inicial:
            # Movimento diagonal para a esquerda e para cima
            for i in range(linha_inicial - 1, linha_final, -1):
                j = coluna_inicial - (linha_inicial - i)
                ocupante = self.getPositionByLinhaColuna(i, j).getOcupante()
                if ocupante is not None and ocupante.getCor() != cor:
                    self.pecasCapturadas.append(ocupante)
                    pecasCapturadasNaRodada.append(ocupante)
                    # self.zerarRodadasSemCaptura()
        if len(pecasCapturadasNaRodada) != 0:
            for peca in pecasCapturadasNaRodada:
                print("Jogador " + peca.jogador.nome + " perdeu uma peça")
                peca.jogador.diminuirPecasEmJogo(peca.dama)
            self.zerarRodadasSemCaptura()
        else:
            self.appendRodadasSemCaptura()

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
        if position.ocupante.dama:
            tamanho = len(self.verificarMovimentosDama(position))
            return tamanho == 0
        else:
            tamanho = len(self.verificarMovimentosPeao(position))
            return tamanho == 0

    def getPlayers(self) -> list[Jogador]:
        lisPlayers = []
        lisPlayers.append(self.jogadorLocal)
        lisPlayers.append(self.jogadorRemoto)
        return lisPlayers

    def avaliarEncerramento(self):
        if self.rodadasSemCaptura == 20:
            self.setStatus(MatchStatus.EMPATE)
            return True
        for jogador in self.getPlayers():
            if not jogador.daVez:
                if len(self.getPositionsWithPiecesOfPlayer(jogador)) == 0:
                    self.setStatus(MatchStatus.VENCEDOR)
                    self.setPerdedor(jogador)
                    print("retornando aqui >> vencedor")
                    return True
                else:
                    pecasBloqueadas: list[Peca] = []
                    # Rever esse algoritimo
                    for position in self.positions:
                        if position.getOcupante() is not None:
                            if position.getOcupante().getJogador() == jogador:
                                if self.pecaBloqueada(position):
                                    pecasBloqueadas.append(position.getOcupante())
                    print("pecasBloqueadas: " + str(len(pecasBloqueadas)))
                    print("pecasEmJogo: " + str(jogador.pecasEmJogo))
                    if len(pecasBloqueadas) == jogador.pecasEmJogo:
                        self.setStatus(MatchStatus.VENCEDOR)
                        self.setPerdedor(jogador)
                        print("retornando aqui >> pecasBloqueadas")
                        return True
                    else:
                        if len(self.lances) >= 5:
                            lancesDama: list[Lance] = []
                            for lance in self.getLances():
                                if lance.getPeca().getDama():
                                    lancesDama.append(lance)
                            if len(lancesDama) == 20:
                                self.setStatus(MatchStatus.EMPATE)
                                print("retornando aqui >> lancesDamas")
                                return True
                            else:
                                if self.rodadasSemCaptura == 10:
                                    empate = self.verificarEmpate()
                                    if empate:
                                        self.setStatus(MatchStatus.EMPATE)
                                        print("retornando aqui >> empate")
                                        return True
                                    else:
                                        print("retornando aqui >> finalElse")
                                        return False

    def verificarEmpate(self):
        # 2 damas contra 2 damas;
        # 2 damas contra uma;
        # 2 damas contra uma dama e uma pedra;
        # uma dama contra uma dama e uma dama contra uma dama e uma pedra, são declarados empatados após 5 lances.
        if len(self.jogadorLocal.getDamas()) == 2 and len(self.jogadorRemoto.getDamas()) == 2:
            return True
        elif len(self.jogadorLocal.getDamas()) == 2 and len(self.jogadorRemoto.getPecasEmJogo()) == 1:
            return True
        elif len(self.jogadorLocal.getDamas()) == 2 and len(self.jogadorRemoto.getDamas()) == 1 and len(
                self.jogadorRemoto.getPecasEmJogo()) == 1:
            return True
        elif len(self.jogadorLocal.getDamas()) == 1 and len(self.jogadorRemoto.getDamas()) == 1 and len(
                self.jogadorLocal.getPecasEmJogo()) == 1 and len(self.jogadorRemoto.getPecasEmJogo()) == 1:
            return True
        else:
            return False

        # pecasLocal: list[Peca] = self.getPlayerPieces(self.jogadorLocal)
        # pecasRemoto: list[Peca] = self.getPlayerPieces(self.jogadorRemoto)
        # if len(pecasLocal) == 2 and len(pecasRemoto) == 2:
        #     damasLocal: list[Peca] = []
        #     for pecaLocal in pecasLocal:
        #         if pecaLocal.getDama():
        #             damasLocal.append(pecaLocal)
        #     damasRemoto: list[Peca] = []
        #     for pecaRemoto in pecasRemoto:
        #         if pecaRemoto.getDama():
        #             damasRemoto.append(pecaRemoto)
        #     if len(damasLocal) == 2 and len(damasRemoto) == 2:
        #         return True
        #     if (len(damasLocal) == 2 and len(damasRemoto) == 1) or (len(damasLocal) == 1 and len(damasRemoto) == 2):
        #         return True
        # else:
        #     return False

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

    def getPosicao(self, lance: Lance) -> Position:
        pass

    def getJogadorConectado(self) -> Jogador:
        pass

    def getJogadorDesconectado(self) -> Jogador:
        pass

    def assumirVencedor(self, lance: Lance):
        pass

    def setStatus(self, status: MatchStatus):
        self.match_status = status

    def getStatus(self) -> MatchStatus:
        return self.match_status

    def getPositions(self) -> list[Position]:
        return self.positions

    def setPositions(self, positions: list[Position]):
        self.positions = positions

    def evaluateEndGame(self, lance: Lance) -> bool:
        pass

    def getRodadasSemCaptura(self) -> int:
        return self.rodadasSemCaptura

    def appendRodadasSemCaptura(self) -> None:
        self.rodadasSemCaptura += 1

    def zerarRodadasSemCaptura(self) -> None:
        self.rodadasSemCaptura = 0

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
            if position.getOcupante() is not None and \
                    position.getOcupante().getJogador().getIdJogador() == jogador.getIdJogador():
                finalList.append(position)
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

    def setPerdedor(self, perdedor: Jogador):
        self.perdedor = perdedor

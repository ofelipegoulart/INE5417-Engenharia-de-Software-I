import uuid
from ast import Dict
import json
import tkinter as tk

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage
from implementacao.CorCasa import CorCasa
from implementacao.CorPeca import CorPeca
from implementacao.Jogador import Jogador
from implementacao.MatchStatus import MatchStatus
from implementacao.Peca import Peca
from implementacao.Position import Position
from tkinter import messagebox

from implementacao.StatusPropostaEmpate import StatusPropostaEmpate
from implementacao.Tabuleiro import Tabuleiro
import jsonpickle


class ActorPlayer(PyNetgamesServerListener):
    def __init__(self, tk):
        super().__init__()
        self.jogo_menu = None
        self.canvas = None
        self.tk = tk
        self.tabuleiro = Tabuleiro(tk)
        self.partidaEmAndamento = False
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 50
        self.WINDOW_WIDTH = 8 * 50
        self.WINDOW_HEIGHT = 8 * 50
        self.retangulos = {}
        self.match_id = None
        self.match_status: int = MatchStatus.EM_ANDAMENTO
        self.server_proxy: PyNetgamesServerProxy = PyNetgamesServerProxy()
        self.construirTabuleiro()

    def construirTabuleiro(self):

        root = self.tk
        menu_bar = tk.Menu(root)
        self.jogo_menu = tk.Menu(menu_bar, tearoff=0)
        self.jogo_menu.add_command(label="Iniciar", command=self.send_connect)
        self.jogo_menu.add_command(label="Desistir")
        self.jogo_menu.add_command(label="Oferecer empate", command=self.oferecerEmpate)
        self.jogo_menu.add_command(label="Sair", command=self.fechar_janela)
        self.jogo_menu.entryconfig("Desistir", state="disable")
        self.jogo_menu.entryconfig("Oferecer empate", state="disable")
        menu_bar.add_cascade(label="Jogo", menu=self.jogo_menu)
        root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        root.title("Damas")

        self.canvas = tk.Canvas(
            root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        self.canvas.pack()

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                if (row + col) % 2 == 0:
                    # self.tabuleiro.positions
                    self.tabuleiro.positions.append(
                        Position(linha=row, coluna=col, cor=CorCasa.BRANCO))

                else:
                    self.tabuleiro.positions.append(
                        Position(linha=row, coluna=col, cor=CorCasa.PRETO))
                    # retangulo = self.canvas.create_rectangle(
                    #     x1, y1, x2, y2, fill="gray", tags=f"square-{row}-{col}")
                # self.retangulos[(row, col)] = retangulo
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 != 0:
                    pecaId = str(row) + str(col)
                    if row < 3:
                        pos = self.tabuleiro.getPositionByLinhaColuna(
                            linha=row, coluna=col)
                        pos.setOcupante(Peca(cor=CorPeca.PRETO, pecaId=pecaId))

                    elif row > 4:
                        self.tabuleiro.getPositionByLinhaColuna(
                            linha=row, coluna=col).ocupante = Peca(cor=CorPeca.VERMELHO, pecaId=pecaId)
        self.montarPositcoes()
        self.add_listener()
        root.config(menu=menu_bar)
        # if status ==

        self.canvas.bind("<Button-1>", self.square_click)
        root.mainloop()

    def oferecerEmpate(self):
        self.square_click(None)

    def square_click(self, event, aceitaPropostaEmpate=None):
        if not self.partidaEmAndamento:
            self.exibir_notificacao("Partida não iniciada")
            return
        if event is None:
            row = None
            col = None
        elif event is not None and aceitaPropostaEmpate is None:
            item_id = event.widget.find_closest(event.x, event.y)[0]
            # Extrai a linha e a coluna do nome da tag do item
            tags = self.canvas.gettags(item_id)
            row, col = [int(x) for x in tags[0].split('-')[1:]]

        # Imprime a linha e a coluna
        temJogada = self.tabuleiro.click(
            linha=row, coluna=col, local_turn=self.tabuleiro.jogadorLocal.daVez,
            aceitaPropostaEmpate=aceitaPropostaEmpate)
        if not temJogada and self.tabuleiro.pecaClicada is None:
            self.montarPositcoes()
            self.exibir_notificacao(self.tabuleiro.errorLocalMessage)
        elif not temJogada and self.tabuleiro.pecaClicada is not None:
            for jogada in self.tabuleiro.getJogadas():
                rectangle = self.retangulos.get(
                    (jogada.getLinha(), jogada.getColuna()))
                if rectangle is not None:
                    self.canvas.itemconfigure(rectangle, fill="yellow")
        elif temJogada:
            # print("Tem jogada é ta tudo None")

            posInicial = self.tabuleiro.getPecaClicada()
            posFinal = self.tabuleiro.getPositionByLinhaColuna(
                linha=row, coluna=col)
            move = {"move": {"positionInicial": jsonpickle.encode(posInicial),
                             "positionFinal": jsonpickle.encode(posFinal),
                             "capturas": jsonpickle.encode(self.tabuleiro.pecasCapturadas),
                             "propostaEmpate": jsonpickle.encode(self.tabuleiro.get_proposta_empate()),
                             "statusPropostaEmpate": jsonpickle.encode(self.tabuleiro.statusPropostaEmpate)}}
            status = self.realizarLance(
                positionInicial=posInicial, positionFinal=posFinal)
            # Verifica se esta recusando uma proposta de empate
            if self.tabuleiro.get_proposta_empate() or posInicial is None:
                move = {"move": {"positionInicial": jsonpickle.encode(posInicial),
                                 "positionFinal": jsonpickle.encode(posFinal),
                                 "capturas": jsonpickle.encode(self.tabuleiro.pecasCapturadas),
                                 "propostaEmpate": jsonpickle.encode(self.tabuleiro.get_proposta_empate()),
                                 "statusPropostaEmpate": jsonpickle.encode(self.tabuleiro.statusPropostaEmpate)}}
            self.tabuleiro.setPecaClicada(None)
            self.server_proxy.send_move(self.match_id, payload=move)

    def aceitarProposta(self, event):
        self.square_click(event=None, aceitaPropostaEmpate=True)

    def recusarProposta(self, event):
        self.square_click(None, False)

    def montarPositcoes(self):
        if self.tabuleiro.match_status == MatchStatus.EMPATE:
            self.canvas.delete("all")  # Limpa todos os elementos do Canvas
            self.canvas.config(bg="white")  # Define o fundo como branco
            self.canvas.create_text(200, 200,
                                    text="Partida empatada! Reinicie a aplicação")  # Cria um texto centralizado
            self.canvas.bind("<Button-1>", self.fechar_janela)
        elif self.tabuleiro.match_status == MatchStatus.VENCEDOR:
            print(self.tabuleiro.perdedor.getIdJogador())
            print(self.tabuleiro.jogadorLocal.getIdJogador())
            playerVencedor = self.tabuleiro.jogadorLocal if \
                self.tabuleiro.perdedor.getIdJogador() == self.tabuleiro.jogadorRemoto.getIdJogador() \
                else self.tabuleiro.jogadorRemoto
            texto_vencedor_player = "Local " if playerVencedor == self.tabuleiro.jogadorLocal else "Remoto "
            texto_vencedor = "venceu! reinicie a aplicação"
            self.canvas.delete("all")  # Limpa todos os elementos do Canvas
            self.canvas.config(bg="white")  # Define o fundo como branco
            self.canvas.create_text(200, 200,
                                    text=texto_vencedor_player + texto_vencedor)  # Cria um texto centralizado
            self.canvas.bind("<Button-1>", self.fechar_janela)
            # for jogador in self.tabuleiro.getPlayers():
            #     if jogador.getVencedor() != False

        elif self.tabuleiro.get_proposta_empate():
            self.jogo_menu.entryconfig("Oferecer empate", state="disable")
            if self.tabuleiro.statusPropostaEmpate == StatusPropostaEmpate.LOCAL_ENVIOU:
                self.canvas.delete("all")  # Limpa todos os elementos do Canvas
                self.canvas.config(bg="white")  # Define o fundo como branco
                self.canvas.create_text(200, 200, text="Aguardando resposta da proposta de empate")
            elif self.tabuleiro.statusPropostaEmpate == StatusPropostaEmpate.REMOTO_ENVIOU:
                self.canvas.delete("all")  # Limpa todos os elementos do Canvas
                self.canvas.config(bg="white")  # Define o fundo como branco
                self.canvas.create_text(200, 200, text="Aceitar proposta de empate?")
                sim = self.canvas.create_text(100, 200, text="Sim", fill="green")
                nao = self.canvas.create_text(50, 200, text="Não", fill="red")
                self.canvas.tag_bind(sim, "<Button-1>", self.aceitarProposta)
                self.canvas.tag_bind(nao, "<Button-1>", self.recusarProposta)
        else:
            # if self.tabuleiro.jogadorLocal is not None:
            #     if not self.tabuleiro.jogadorLocal.daVez():
            #         self.jogo_menu.entryconfig("Oferecer empate", state="disabled")
            self.canvas.delete("all")  # Limpa todos os elementos do Canvas
            for position in self.tabuleiro.getPositions():
                x1 = position.getColuna() * self.SQUARE_SIZE
                y1 = position.getLinha() * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE

                if position.getCasa() == CorCasa.PRETO:
                    retangulo = self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="gray", tags=f"square-{position.getLinha()}-{position.getColuna()}")
                else:  # Casa branca
                    retangulo = self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="white", tags=f"square-{position.getLinha()}-{position.getColuna()}")
                self.retangulos[(position.getLinha(),
                                 position.getColuna())] = retangulo
                piece_size = self.SQUARE_SIZE // 2
                if position.getOcupante() is not None:
                    if position.getOcupante().getCor() == CorPeca.VERMELHO:
                        if position.getOcupante().getDama():
                            self.canvas.create_oval(position.getColuna() * self.SQUARE_SIZE + piece_size // 2,
                                                    position.getLinha() * self.SQUARE_SIZE + piece_size // 2,
                                                    position.getColuna() * self.SQUARE_SIZE + self.SQUARE_SIZE - piece_size // 2,
                                                    position.getLinha() * self.SQUARE_SIZE + self.SQUARE_SIZE - piece_size // 2,
                                                    fill="orange",
                                                    tags=f"square-{position.getLinha()}-{position.getColuna()}")
                        else:

                            self.canvas.create_oval(position.getColuna() * self.SQUARE_SIZE + piece_size // 2,
                                                    position.getLinha() * self.SQUARE_SIZE + piece_size // 2,
                                                    position.getColuna() * self.SQUARE_SIZE + self.SQUARE_SIZE - piece_size // 2,
                                                    position.getLinha() * self.SQUARE_SIZE + self.SQUARE_SIZE - piece_size // 2,
                                                    fill="red",
                                                    tags=f"square-{position.getLinha()}-{position.getColuna()}")

                    else:
                        if position.getOcupante().getDama():
                            self.canvas.create_oval(position.getColuna() * self.SQUARE_SIZE + piece_size // 2,
                                                    position.getLinha() * self.SQUARE_SIZE + piece_size // 2,
                                                    position.getColuna() * self.SQUARE_SIZE + self.SQUARE_SIZE - piece_size // 2,
                                                    position.getLinha() * self.SQUARE_SIZE + self.SQUARE_SIZE - piece_size // 2,
                                                    fill="blue",
                                                    tags=f"square-{position.getLinha()}-{position.getColuna()}")
                        else:
                            self.canvas.create_oval(position.getColuna() * self.SQUARE_SIZE + piece_size // 2,
                                                    position.getLinha() * self.SQUARE_SIZE + piece_size // 2,
                                                    position.getColuna() * self.SQUARE_SIZE + self.SQUARE_SIZE - piece_size // 2,
                                                    position.getLinha() * self.SQUARE_SIZE + self.SQUARE_SIZE - piece_size // 2,
                                                    fill="black",
                                                    tags=f"square-{position.getLinha()}-{position.getColuna()}")

    def exibir_notificacao(self, message: str):
        messagebox.showinfo("Notificação de erro", message=message)

    def fechar_janela(self, event):
        self.tk.destroy()

    def realizarLance(self, positionInicial: Position, positionFinal: Position):
        if not self.tabuleiro.get_proposta_empate():
            if positionInicial is not None:
                position = self.tabuleiro.getPositionByLinhaColuna(
                    positionFinal.getLinha(), positionFinal.getColuna())
                posInitial = self.tabuleiro.getPositionByLinhaColuna(
                    positionInicial.getLinha(), positionInicial.getColuna())
                # identifica se teve captura
                    # Verifica se a casa selecionada é uma ponta do tabuleiro
                if (positionFinal.getLinha() == 0 and posInitial.getOcupante().getCor() == CorPeca.VERMELHO) or (
                        positionFinal.getLinha() == 7 and posInitial.getOcupante().getCor() == CorPeca.PRETO):
                    posInitial.getOcupante().setDama(True)
                    # Transforma peça em dama
                position.setOcupante(positionInicial.getOcupante())
                self.tabuleiro.verificaCapturas(positionInicial, positionFinal, positionInicial.getOcupante().getCor())
                self.tabuleiro.removerPecas()
                posInitial.setOcupante(None)
                partidaEncerrada = self.tabuleiro.avaliarEncerramento()
                if not partidaEncerrada:
                    self.tabuleiro.trocarTurnos()
                    if self.tabuleiro.jogadorLocal.daVez:
                        self.jogo_menu.entryconfig("Oferecer empate", state="normal")
                    else:
                        self.jogo_menu.entryconfig("Oferecer empate", state="disable")
                self.montarPositcoes()
                return self.tabuleiro.match_status
            # Proposta de empate recusada
            else:
                if self.tabuleiro.jogadorLocal.daVez:
                    self.jogo_menu.entryconfig("Oferecer empate", state="normal")
                else:
                    self.jogo_menu.entryconfig("Oferecer empate", state="disable")
                # self.tabuleiro.trocarTurnos()
                self.montarPositcoes()
        elif self.tabuleiro.get_proposta_empate():
            if self.tabuleiro.statusPropostaEmpate == StatusPropostaEmpate.LOCAL_ACEITOU or \
                    self.tabuleiro.statusPropostaEmpate == StatusPropostaEmpate.REMOTO_ACEITOU:
                print("Chegando aqui >> proposta de empate aceita")
                self.tabuleiro.setStatus(MatchStatus.EMPATE)
                self.montarPositcoes()
                return MatchStatus.EMPATE
            else:
                if self.tabuleiro.statusPropostaEmpate == StatusPropostaEmpate.LOCAL_ENVIOU or \
                        self.tabuleiro.statusPropostaEmpate == StatusPropostaEmpate.REMOTO_ENVIOU:
                    self.tabuleiro.setStatus(MatchStatus.EM_ANDAMENTO)
                    self.montarPositcoes()
                    return MatchStatus.EM_ANDAMENTO
                else:
                    self.tabuleiro.set_proposta_empate(False)
                    self.tabuleiro.statusPropostaEmpate = StatusPropostaEmpate.SEM_PROPOSTA
                    self.montarPositcoes()
                    return MatchStatus.EM_ANDAMENTO

    def add_listener(self):
        self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

        # self.jogo_menu.entryconfig("Desistir", state="disable")
        self.jogo_menu.entryconfig("Oferecer empate", state="disable")

    def send_connect(self):
        self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

    def receive_connection_success(self):
        print('**************************CONECTADO********************')
        self.jogo_menu.entryconfig("Iniciar", state="disable")
        self.send_match()

    def send_match(self):
        self.server_proxy.send_match(2)

    def receive_disconnect(self):
        self.exibir_notificacao("Remoto desconectou, fechando")
        exit()

    def receive_error(self, error: Exception):
        self.exibir_notificacao("Erro no servidor, fechando")
        exit()

    def receive_match(self, message: MatchStartedMessage):
        self.jogo_menu.entryconfig("Desistir", state="normal")
        self.jogo_menu.entryconfig("Oferecer empate", state="normal")
        self.partidaEmAndamento = True
        self.match_id = message.match_id
        print("RECEBEU PARTIDA")
        initialPosition = message.position
        if initialPosition == 1:
            print('position 1')
            pecasLocal: list[Peca] = []
            pecasRemoto: list[Peca] = []
            for position in self.tabuleiro.positions:
                if position.ocupante is not None:
                    peca = position.ocupante
                    if position.ocupante.getCor() == CorPeca.VERMELHO:
                        position.getOcupante().setJogador(self.tabuleiro.jogadorLocal)
                        position.getOcupante().getJogador().setNome("Vermelho")
                        pecasLocal.append(peca)
                    if position.ocupante.getCor() == CorPeca.PRETO:
                        position.getOcupante().setJogador(self.tabuleiro.jogadorRemoto)
                        position.getOcupante().getJogador().setNome("Preto")
                        pecasRemoto.append(peca)
            self.tabuleiro.jogadorLocal.pecas = pecasLocal
            self.tabuleiro.jogadorLocal.daVez = True
            self.tabuleiro.jogadorLocal.setIdJogador(initialPosition == 1)
            self.tabuleiro.jogadorRemoto.pecas = pecasRemoto
            self.tabuleiro.jogadorRemoto.daVez = False
            self.tabuleiro.jogadorRemoto.setIdJogador(initialPosition == 0)
        elif initialPosition == 0:
            print('position 0')
            pecasRemoto: list[Peca] = []
            pecasLocal: list[Peca] = []
            for position in self.tabuleiro.positions:
                if position.ocupante != None:
                    peca = position.ocupante
                    if position.ocupante.getCor() == CorPeca.VERMELHO:
                        position.getOcupante().setJogador(self.tabuleiro.jogadorRemoto)
                        position.getOcupante().getJogador().setNome("Vermelho")
                        pecasRemoto.append(peca)
                    if position.ocupante.getCor() == CorPeca.PRETO:
                        position.getOcupante().setJogador(self.tabuleiro.jogadorLocal)
                        position.getOcupante().getJogador().setNome("Preto")
                        pecasLocal.append(peca)
            self.tabuleiro.jogadorLocal.pecas = pecasLocal
            self.tabuleiro.jogadorLocal.daVez = False
            self.tabuleiro.jogadorLocal.setIdJogador(initialPosition == 0)
            self.tabuleiro.jogadorRemoto.pecas = pecasRemoto
            self.tabuleiro.jogadorRemoto.daVez = True
            self.tabuleiro.jogadorRemoto.setIdJogador(initialPosition == 1)
        if self.tabuleiro.jogadorLocal.daVez:
            self.jogo_menu.entryconfig("Oferecer empate", state="normal")
        else:
            self.jogo_menu.entryconfig("Oferecer empate", state="disable")

        # for jogador in self.tabuleiro.getPlayers():
        #     if jogador.daVez == False:

        # for peca in self.tabuleiro.jogadorLocal.pecas:
        #     # if position.ocupante is not None:

    def receive_move(self, move: MoveMessage):
        positionInitial = jsonpickle.decode(
            move.payload.get("move").get("positionInicial"))

        positionFinal = jsonpickle.decode(
            move.payload.get("move").get("positionFinal"))
        self.tabuleiro.pecasCapturadas = jsonpickle.decode(
            move.payload.get("move").get("capturas"))
        propostaEmpate = jsonpickle.decode(move.payload.get("move").get("propostaEmpate"))
        statusPropostaEmpate = jsonpickle.decode(move.payload.get("move").get("statusPropostaEmpate"))
        if propostaEmpate:
            self.tabuleiro.set_proposta_empate(True)
            if statusPropostaEmpate == StatusPropostaEmpate.LOCAL_ENVIOU:
                self.tabuleiro.statusPropostaEmpate = StatusPropostaEmpate.REMOTO_ENVIOU
            if statusPropostaEmpate == StatusPropostaEmpate.LOCAL_ACEITOU:
                self.tabuleiro.statusPropostaEmpate = StatusPropostaEmpate.REMOTO_ACEITOU
            self.realizarLance(positionInicial=positionInitial,
                               positionFinal=positionFinal)
        else:
            self.tabuleiro.set_proposta_empate(False)
            self.tabuleiro.statusPropostaEmpate = StatusPropostaEmpate.SEM_PROPOSTA
            self.realizarLance(positionInicial=positionInitial,
                               positionFinal=positionFinal)

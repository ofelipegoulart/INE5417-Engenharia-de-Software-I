import tkinter as tk

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage
from implementacao.CorCasa import CorCasa
from implementacao.CorPeca import CorPeca
from implementacao.Jogador import Jogador
from implementacao.Peca import Peca
from implementacao.Position import Position
from tkinter import messagebox
from implementacao.Tabuleiro import Tabuleiro


class ActorPlayer(PyNetgamesServerListener):
    def __init__(self, tk):
        super().__init__()
        self.canvas = None
        self.tk = tk
        self.tabuleiro = Tabuleiro(tk)
        self.partidaEmAndamento = False
        self.construirTabuleiro()

    def construirTabuleiro(self):
        BOARD_SIZE = 8
        SQUARE_SIZE = 50
        WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
        WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE

        root = self.tk
        menu_bar = tk.Menu(root)
        self.retangulos = {}
        self.jogo_menu = tk.Menu(menu_bar, tearoff=0)
        self.jogo_menu.add_command(label="Iniciar", command=self.send_connect)
        self.jogo_menu.add_command(label="Desistir")
        self.jogo_menu.add_command(label="Oferecer empate")
        self.jogo_menu.add_command(label="Sair", command=self.fechar_janela)
        self.jogo_menu.entryconfig("Desistir", state="disable")
        self.jogo_menu.entryconfig("Oferecer empate", state="disable")
        menu_bar.add_cascade(label="Jogo", menu=self.jogo_menu)
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        root.title("Damas")

        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                if (row + col) % 2 == 0:
                    # self.tabuleiro.positions
                    self.tabuleiro.positions.append(
                        Position(linha=row, coluna=col, cor=CorCasa.BRANCO))
                    retangulo = self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="white", tags=f"square-{row}-{col}")
                else:
                    self.tabuleiro.positions.append(
                        Position(linha=row, coluna=col, cor=CorCasa.PRETO))
                    retangulo = self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="gray", tags=f"square-{row}-{col}")
                self.retangulos[(row, col)] = retangulo

        piece_size = SQUARE_SIZE // 2
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 != 0:
                    if row < 3:
                        pos = self.tabuleiro.getPositionByLinhaColuna(
                            linha=row, coluna=col)
                        pos.ocupante = Peca(cor=CorPeca.PRETO)
                        self.canvas.create_oval(col * SQUARE_SIZE + piece_size // 2,
                                                row * SQUARE_SIZE + piece_size // 2,
                                                col * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                                                row * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                                                fill="black", tags=f"square-{row}-{col}")
                    elif row > 4:
                        self.tabuleiro.getPositionByLinhaColuna(
                            linha=row, coluna=col).ocupante = Peca(cor=CorPeca.VERMELHO)
                        self.canvas.create_oval(col * SQUARE_SIZE + piece_size // 2,
                                                row * SQUARE_SIZE + piece_size // 2,
                                                col * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                                                row * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                                                fill="red", tags=f"square-{row}-{col}")

        self.add_listener()
        root.config(menu=menu_bar)

        def square_click(event):
            if not self.partidaEmAndamento:
                return
            item_id = event.widget.find_closest(event.x, event.y)[0]
            # current_color = self.canvas.itemcget(item_id, "fill")
            # if current_color == "yellow":
            #     return
            new_color = "yellow"
            # self.canvas.itemconfigure(item_id, fill=new_color)
            # self.canvas.after(500, lambda: self.canvas.itemconfigure(
            #     item_id, fill=current_color))

            # Extrai a linha e a coluna do nome da tag do item
            tags = self.canvas.gettags(item_id)
            row, col = [int(x) for x in tags[0].split('-')[1:]]

            # Imprime a linha e a coluna
            print("Linha:", row)
            print("Coluna:", col)
            temJogada = self.tabuleiro.click(
                linha=row, coluna=col, local_turn=self.tabuleiro.jogadorLocal.daVez)
            if not temJogada and self.tabuleiro.pecaClicada is None:
                self.exibir_notificacao(self.tabuleiro.errorLocalMessage)
            elif not temJogada and self.tabuleiro.pecaClicada is not None:
                for jogada in self.tabuleiro.getJogadas():
                    # self.canvas.itemconfigure(self.retangulos[jogada.linha, jogada.linha], fill="yellow")
                    rectangle = self.retangulos.get(
                        (jogada.getLinha(), jogada.getColuna()))
                    if rectangle is not None:
                        self.canvas.itemconfigure(rectangle, fill="yellow")
            elif temJogada:
                print("casa clicada inicial -> ", self.tabuleiro.getPecaClicada().getColuna(), self.tabuleiro.getPecaClicada().getLinha())
                # self.realizarLance()
                # for jogada in self.tabuleiro.getJogadas():
                #     rectangle = self.retangulos.get(
                #         (jogada.getLinha(), jogada.getColuna()))
                #     if rectangle is not None:
                #         self.canvas.itemconfigure(rectangle, fill="gray")
                #
                # self.tabuleiro.getPecaClicada().setColuna(col)
                # self.tabuleiro.getPecaClicada().setLinha(row)
                # rectangle = self.retangulos.get((self.tabuleiro.getPecaClicada().getLinha(),
                #                                  self.tabuleiro.getPecaClicada().getColuna()))
                # self.canvas.itemconfigure(
                #     rectangle, fill="gray", tags=f"square-{row}-{col}")
                # self.canvas.create_oval(col * SQUARE_SIZE + piece_size // 2,
                #                         row * SQUARE_SIZE + piece_size // 2,
                #                         col * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                #                         row * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                #                         fill="red", tags=f"square-{row}-{col}")
                # self.tabuleiro.setPecaClicada(None)
        self.canvas.bind("<Button-1>", square_click)
        root.mainloop()

    def exibir_notificacao(self, message: str):
        messagebox.showinfo("Notificação de erro", message=message)

    def fechar_janela(self):
        self.tk.destroy()

    # def realizarLance(self, row, ):
    #     if not self.tabuleiro.get_proposta_empate():


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
        pass

    def receive_error(self, error: Exception):
        pass

    def receive_match(self, message: MatchStartedMessage):
        self.jogo_menu.entryconfig("Desistir", state="normal")
        self.jogo_menu.entryconfig("Oferecer empate", state="normal")
        self.partidaEmAndamento = True
        print("RECEBEU PARTIDA")
        initialPosition = message.position
        # print(message.position)  position = 1 or position = 0 - position 1: comeca jogando, position 0: espera
        if initialPosition == 1:
            print('position 1')
            pecasLocal: list[Peca] = []
            pecasRemoto: list[Peca] = []
            for position in self.tabuleiro.positions:
                if position.ocupante != None:
                    peca = position.ocupante
                    if position.ocupante.getCor() == CorPeca.VERMELHO:
                        position.getOcupante().setJogador(self.tabuleiro.jogadorLocal)
                        pecasLocal.append(peca)
                    if position.ocupante.getCor() == CorPeca.PRETO:
                        position.getOcupante().setJogador(self.tabuleiro.jogadorRemoto)
                        pecasRemoto.append(peca)
            self.tabuleiro.jogadorLocal.pecas = pecasLocal
            self.tabuleiro.jogadorLocal.daVez = True
            self.tabuleiro.jogadorRemoto.pecas = pecasRemoto
            self.tabuleiro.jogadorRemoto.daVez = False
        elif initialPosition == 0:
            print('position 0')
            pecasRemoto: list[Peca] = []
            pecasLocal: list[Peca] = []
            for position in self.tabuleiro.positions:
                if position.ocupante != None:
                    peca = position.ocupante
                    if position.ocupante.getCor() == CorPeca.VERMELHO:
                        position.getOcupante().setJogador(self.tabuleiro.jogadorRemoto)
                        pecasRemoto.append(peca)
                    if position.ocupante.getCor() == CorPeca.PRETO:
                        position.getOcupante().setJogador(self.tabuleiro.jogadorLocal)
                        pecasLocal.append(peca)
            self.tabuleiro.jogadorLocal.pecas = pecasLocal
            self.tabuleiro.jogadorLocal.daVez = False
            self.tabuleiro.jogadorRemoto.pecas = pecasRemoto
            self.tabuleiro.jogadorRemoto.daVez = True

        # for jogador in self.tabuleiro.getPlayers():
        #     if jogador.daVez == False:

        # for peca in self.tabuleiro.jogadorLocal.pecas:
        #     # if position.ocupante is not None:
        #     #     print(position.ocupante.cor)
        #     print(peca.cor)
        #     # else:
        #     #     print("sem peca")

    def receive_move(self, move):
        pass

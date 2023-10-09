import tkinter as tk

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener


class ActorPlayer(PyNetgamesServerListener):
    def __init__(self, tk):
        super().__init__()
        self.canvas = None
        self.tk = tk
        self.partidaEmAndamento = False
        self.construirTabuleiro()

    def construirTabuleiro(self):
        BOARD_SIZE = 8
        SQUARE_SIZE = 50
        WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
        WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE

        root = self.tk
        menu_bar = tk.Menu(root)
        self.jogo_menu = tk.Menu(menu_bar, tearoff=0)
        # self.jogo_menu.add_command(label="Iniciar", command=self.send_connect)
        # self.jogo_menu.add_command(label="Desistir")
        # self.jogo_menu.add_command(label="Oferecer empate")
        self.jogo_menu.add_command(label="Sair", command=self.fechar_janela)
        # self.jogo_menu.entryconfig("Desistir", state="disable")
        # self.jogo_menu.entryconfig("Oferecer empate", state="disable")
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
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")

        piece_size = SQUARE_SIZE // 2
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 != 0:
                    if row < 3:
                        self.canvas.create_oval(col * SQUARE_SIZE + piece_size // 2,
                                           row * SQUARE_SIZE + piece_size // 2,
                                           col * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                                           row * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                                           fill="black")
                    elif row > 4:
                        self.canvas.create_oval(col * SQUARE_SIZE + piece_size // 2,
                                           row * SQUARE_SIZE + piece_size // 2,
                                           col * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                                           row * SQUARE_SIZE + SQUARE_SIZE - piece_size // 2,
                                           fill="red")

        self.add_listener()
        self.send_connect()
        root.config(menu=menu_bar)

        def square_click(event):
            if not self.partidaEmAndamento:
                return
            item_id = event.widget.find_closest(event.x, event.y)[0]
            current_color = self.canvas.itemcget(item_id, "fill")
            if current_color == "yellow":
                return
            new_color = "yellow"
            self.canvas.itemconfigure(item_id, fill=new_color)
            self.canvas.after(500, lambda: self.canvas.itemconfigure(item_id, fill=current_color))
        self.canvas.bind("<Button-1>", square_click)
        root.mainloop()

    def fechar_janela(self):
        self.tk.destroy()

    def add_listener(self):
        self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

        # self.jogo_menu.entryconfig("Desistir", state="disable")
        # self.jogo_menu.entryconfig("Oferecer empate", state="disable")

    def send_connect(self):
        self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

    def receive_connection_success(self):
        print('**************************CONECTADO********************')
        # self.jogo_menu.entryconfig("Iniciar", state="disable")
        self.send_match()

    def send_match(self):
        self.server_proxy.send_match(2)

    def receive_disconnect(self):
        pass

    def receive_error(self, error: Exception):
        pass

    def receive_match(self, match):
        # self.jogo_menu.entryconfig("Desistir", state="normal")
        # self.jogo_menu.entryconfig("Oferecer empate", state="normal")
        self.partidaEmAndamento = True
        print("RECEBEU PARTIDA")

    def receive_move(self, move):
        pass

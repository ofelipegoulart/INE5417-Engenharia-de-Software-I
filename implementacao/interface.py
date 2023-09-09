import tkinter as tk


class ActorPlayer():
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
        self.jogo_menu.add_command(label="Oferecer empate")
        self.jogo_menu.add_command(label="Sair", command=self.fechar_janela)
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
        root.config(menu=menu_bar)

        def square_click(event):
            print("click:")
            print("casa x: " + str(event.x))
            print("casa y: " + str(event.y))
            print("-------------------------------------")
            # if not self.partidaEmAndamento:
            #     return
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
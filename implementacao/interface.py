import tkinter as tk


class Tabuleiro:
    def __init__(self, tk):
        self.canvas = None
        self.partidaEmAndamento = False
        self.tk = tk
        self.construirTabuleiro()

    def construirTabuleiro(self):
        BOARD_SIZE = 8
        SQUARE_SIZE = 50
        WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
        WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE

        root = self.tk
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

        # def square_click(event):
        #     item_id = event.widget.find_closest(event.x, event.y)[0]
        #     current_color = self.canvas.itemcget(item_id, "fill")
        #     if current_color == "yellow":
        #         return
        #     new_color = "yellow"
        #     self.canvas.itemconfigure(item_id, fill=new_color)
        #     self.canvas.after(500, lambda: self.canvas.itemconfigure(item_id, fill=current_color))
        #
        # for item_id in self.canvas.find_all():
        #     self.canvas.tag_bind(item_id, "<Button-1>", square_click)

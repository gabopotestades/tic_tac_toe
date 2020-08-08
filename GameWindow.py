import tkinter as tk

class Game:
    def __init__(self, master, rationality):
        self.master = master
        self.rationality = rationality
        self.master.title("Tic Tac Toe")

        self.master.minsize(width = 400, height = 400)
        self.master.resizable(width = False, height = False)
        #self.frame = tk.Frame(self.master)

        label = tk.Label(self.master, text=('{0}: {1}').format('Rationality', self.rationality))
        label.config(font=("Adobe Song Std L", 30))
        label.grid(row=0, columnspan=4, ipadx=40, ipady=20)



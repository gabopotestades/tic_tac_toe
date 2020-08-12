import tkinter as tk
from PlayRandomly import RandomStrategy

class Game:

    def __init__(self, master, rationality):
        
        #Setup grid
        self.master = master
        self.rationality = rationality
        self.master.title("Tic Tac Toe")
        self.master.resizable(width = False, height = False)
        self.w_height = 300
        self.w_width = self.w_height * 2
        self.canvas = tk.Canvas(self.master, width=self.w_width, height=self.w_height, borderwidth=0, highlightthickness=0, background="#a2d6ec")
        self.canvas.pack(side="top", fill="both", expand="true")

        #Number of rows and columns
        self.rows = 3
        self.columns = 3

        #Additional properties
        image_reduce_size = 16
        self.result = "on-going"
        self.x_color = "#5f719d"
        self.x_pic_orig = tk.PhotoImage(file="x_pic.png")
        self.x_pic = self.x_pic_orig.subsample(image_reduce_size,image_reduce_size)
        self.o_color = "#494f83"
        self.o_pic_orig = tk.PhotoImage(file="o_pic.png")
        self.o_pic = self.o_pic_orig.subsample(image_reduce_size,image_reduce_size)
        
        #List of tiles
        self.tiles = {}
        self.canvas.bind("<Configure>", self.redraw)
        
        #Update history
        self.action_history = tk.Text(self.canvas)
        self.canvas.create_window(450, 120, window = self.action_history, height = 220, width = 280)
        self.action_history.bind("<1>", lambda event: self.action_history.focus_set())
        self.tiles_history = [['a', 'b', 'c'], 
                              ['d', 'e', 'f'], 
                              ['g', 'h', 'i']]
        self.shape_history = {}
        self.available_moves = []

        #Turn config
        self.turn = "X"
        self.first_turn = "X"
        self.print_to_game_log("X's turn first\n")
        self.x_turns = 0
        self.o_turns = 0

        #Setup buttons
        self.btnNewGame = tk.Button(self.canvas, text = "New Game", command = self.new_game, width = 10)
        self.canvas.create_window(380, 270, window = self.btnNewGame)

        self.btnQuit = tk.Button(self.canvas, text = "Quit", command = self.quit_game, width = 10)
        self.canvas.create_window(520, 270, window = self.btnQuit)

        #Set rationality for testing
        self.rationality = 1

    #Function to draw grid
    def redraw(self, event=None):
        self.canvas.delete("rect")
        cellwidth = int((self.canvas.winfo_width() / 2)/self.columns)
        cellheight = int(self.canvas.winfo_height()/self.columns)
        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column*cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight
                tile = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#8cb4d2", tags="rect")
                self.tiles[row,column] = tile
                self.available_moves.append((row,column))
                self.canvas.tag_bind(tile, "<1>", lambda event, row=row, column=column: self.clicked(row, column))

    #Function to change tile symbol
    def clicked(self, row, column):
        tile = self.tiles[row,column]
        tile_color = self.canvas.itemcget(tile, "fill")

        if tile_color == "#8cb4d2":

            self.tiles_history[row][column] = self.turn
            history = "{0} placed on ({1}, {2})\n".format(self.turn, row, column)
            self.print_to_game_log(history)

            coordinates = self.canvas.coords(tile)
            coord_x = coordinates[0] + int(((self.canvas.winfo_width() / 2)/self.columns) / 2)
            coord_y = coordinates[1] + int((self.canvas.winfo_height()/self.columns) / 2)
            
            #Player's turn
            self.turn = "O"
            self.x_turns += 1
            self.shape_history[row, column] = self.canvas.create_image(coord_x, coord_y, image = self.x_pic)
            self.canvas.itemconfigure(tile, fill=self.x_color)
            self.available_moves.remove((row, column)) 

            if self.is_winner():
                self.end_game("win")
            elif len(self.shape_history) == 9:
                self.end_game("draw")
            else:
                #After player turn, AI's turn will activate
                self.AI_turn()       

    #AI's strategy
    def AI_turn(self):

        if self.rationality == 1:
            randomStrat = RandomStrategy(self.available_moves).random_move()
            row = randomStrat[0]
            column = randomStrat[1]
            self.available_moves.remove(randomStrat)

        #Get tile object using coordinates
        tile = self.tiles[row,column]

        #Get coordinates of tile to insert image
        coordinates = self.canvas.coords(tile)
        coord_x = coordinates[0] + int(((self.canvas.winfo_width() / 2)/self.columns) / 2)
        coord_y = coordinates[1] + int((self.canvas.winfo_height()/self.columns) / 2)

        #Insert move to game log
        log = "{0} placed on ({1}, {2})\n".format(self.turn, row, column)
        self.print_to_game_log(log)
        
        self.canvas.itemconfigure(tile, fill=self.o_color)
        self.tiles_history[row][column] = self.turn
        self.shape_history[row, column] = self.canvas.create_image(coord_x, coord_y, image = self.o_pic)

        self.turn = "X"
        self.o_turns += 1   

        if self.is_winner():
            self.end_game("win")
        elif len(self.shape_history) == 9:
            self.end_game("draw")

    #Bool to check if someone wins
    def is_winner(self):
        return ((self.tiles_history[0][0] == self.tiles_history[0][1] == self.tiles_history[0][2]) or #Upper Row
            (self.tiles_history[1][0] == self.tiles_history[1][1] == self.tiles_history[1][2]) or #Middle Row
            (self.tiles_history[2][0] == self.tiles_history[2][1] == self.tiles_history[2][2]) or #Bottom Row

            (self.tiles_history[0][0] == self.tiles_history[1][0] == self.tiles_history[2][0]) or #Left Column
            (self.tiles_history[0][1] == self.tiles_history[1][1] == self.tiles_history[2][1]) or #Middle Column
            (self.tiles_history[0][2] == self.tiles_history[1][2] == self.tiles_history[2][2]) or #Right Column
            
            #Upper Left to Bottom Right Diagonal
            (self.tiles_history[0][0] == self.tiles_history[1][1] == self.tiles_history[2][2]) or 
            #Bottom Left to Upper Right Diagonal
            (self.tiles_history[0][2] == self.tiles_history[1][1] == self.tiles_history[2][0]))

    #Check if someone has already won
    def end_game(self, mode):
        if mode == "draw":
            self.print_to_game_log("It's a draw.\n")
        else:
            winner = 'X' if self.turn == 'O' else 'O'
            for tile in self.tiles.values():
                if self.canvas.itemcget(tile, "fill") == "#8cb4d2":
                    self.canvas.itemconfigure(tile, fill="#a2d6ec")
            self.print_to_game_log((winner + " has won!\n"))

    #Print to game log
    def print_to_game_log(self, log):
        self.action_history.config(state="normal")
        self.action_history.insert("end", log)
        self.action_history.config(state="disabled")

    #Reset board
    def new_game(self):

        for shape in self.shape_history.values():
            self.canvas.delete(shape)
        self.action_history.config(state="normal")
        self.action_history.delete("1.0", tk.END)
        self.x_turns = 0
        self.o_turns = 0
        self.tiles_history = [['a', 'b', 'c'], 
                              ['d', 'e', 'f'], 
                              ['g', 'h', 'i']]
        self.available_moves = []
        self.shape_history = {}
        
        if self.first_turn == "X":
            self.first_turn = "O"
            self.turn = "O"
        else:
            self.first_turn = "X"
            self.turn = "X"

        self.action_history.insert("end", (self.first_turn + "'s turn first\n"))
        self.action_history.config(state="disabled")

        for column in range(self.columns):
            for row in range(self.rows):
                tile = self.tiles[row,column]
                self.available_moves.append((row,column))
                self.canvas.itemconfigure(tile, fill="#8cb4d2")
        
        if self.first_turn == "O":
            self.AI_turn()

    #Quit the program
    def quit_game(self):
        self.master.quit()
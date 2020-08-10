import tkinter as tk

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
        self.x_pic_orig = tk.PhotoImage(file="x_pic.png")
        self.x_pic = self.x_pic_orig.subsample(image_reduce_size,image_reduce_size)
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

        #Turn config
        self.turn = "X"
        self.first_turn = "X"
        self.action_history.insert("end", "X's turn first\n")
        self.action_history.config(state="disabled")
        self.x_turns = 0
        self.o_turns = 0

        #Setup buttons
        self.btnNewGame = tk.Button(self.canvas, text = "New Game", command = self.new_game, width = 10)
        self.canvas.create_window(380, 270, window = self.btnNewGame)

        self.btnQuit = tk.Button(self.canvas, text = "Quit", command = self.quit_game, width = 10)
        self.canvas.create_window(520, 270, window = self.btnQuit)

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
                self.canvas.tag_bind(tile, "<1>", lambda event, row=row, column=column: self.clicked(row, column))

    def clicked(self, row, column):
        tile = self.tiles[row,column]
        tile_color = self.canvas.itemcget(tile, "fill")
        coordinates = self.canvas.coords(tile)
        coord_x = coordinates[0] + int(((self.canvas.winfo_width() / 2)/self.columns) / 2)
        coord_y = coordinates[1] + int((self.canvas.winfo_height()/self.columns) / 2)

        if tile_color == "#8cb4d2":

            history = "{0} placed on ({1}, {2})\n"

            self.action_history.config(state="normal")
            self.action_history.insert("end", history.format(self.turn, row, column))
            self.action_history.config(state="disabled")
            self.tiles_history[row][column] = self.turn
            
            if self.turn == "X":
                self.turn = "O"
                self.x_turns += 1
                new_color = "#5f719d"
                self.shape_history[row, column] = self.canvas.create_image(coord_x, coord_y,
                image = self.x_pic)
            elif self.turn == "O":
                self.turn = "X"
                self.o_turns += 1
                new_color = "#494f83"
                self.shape_history[row, column] = self.canvas.create_image(coord_x, coord_y,
                image = self.o_pic)

            self.canvas.itemconfigure(tile, fill=new_color)
        
            #Check winner
            if len(self.shape_history) > 4:
                winner = 'X' if self.turn == 'O' else 'O'
                if self.is_winner():
                    for tile in self.tiles.values():
                        if self.canvas.itemcget(tile, "fill") == "#8cb4d2":
                            self.canvas.itemconfigure(tile, fill="#a2d6ec")
                    self.action_history.config(state="normal")   
                    self.action_history.insert("end", (winner + " has won!\n"))
                    self.action_history.config(state="disabled")
                elif len(self.shape_history) == 9:
                    self.action_history.config(state="normal")   
                    self.action_history.insert("end", ("It's a draw.\n"))
                    self.action_history.config(state="disabled")


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
                self.canvas.itemconfigure(tile, fill="#8cb4d2")

    def quit_game(self):
        self.master.quit()
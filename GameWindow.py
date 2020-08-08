import tkinter as tk

class Game:
    def __init__(self, master, rationality):
        
        #Setup grid
        self.master = master
        self.rationality = rationality
        self.master.title("Tic Tac Toe")
        self.master.resizable(width = False, height = False)
        self.canvas = tk.Canvas(self.master, width=600, height=300, borderwidth=0, highlightthickness=0, background="#7693b8")
        self.canvas.pack(side="top", fill="both", expand="true")

        #Number of rows and columns
        self.rows = 3
        self.columns = 3
        
        #List of tiles
        self.tiles = {}
        self.canvas.bind("<Configure>", self.redraw)
        
        #Update history
        #self.strActions = tk.StringVar()
        #self.action_history = tk.Text(self.master, width = 300, height = 300)
        #self.action_history.pack(side="right")
        #self.status = tk.Label(self.master, anchor="w")
        #self.status.pack(side="bottom", fill="x")
        

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
        new_color = "#8cb4d2" if  tile_color == "#494f83" else "#494f83"
        self.canvas.itemconfigure(tile, fill=new_color)
        #self.status.configure(text="you clicked on %s/%s" % (row, column))



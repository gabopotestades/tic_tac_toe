from GameWindow import Game
import tkinter as tk

class Main(tk.Frame):
    
    # initialize class
    def __init__(self, master):
        self.master = master
    
        # initialize tkinter variables
        self.rationalityVar = tk.IntVar() # holds the selected rationality level
        self.errorMessageVar = tk.StringVar() # holds the error message to display
            
        self.master.title("Tic-Tac-Toe") 
        self.master.minsize(width = 200, height = 360)
        self.master.resizable(width = False, height = False)
        self.master.config(bg = "#a2d6ec")
        
        self.create_widgets()
        
    def closed_window_callback(topLevel):
        # destroy the instantiated TopLevel widget and restore this root window
        topLevel.newWindow.destroy()
        root.deiconify()
        
    def create_widgets(self):
         # set overall color
        # taken from https://www.color-hex.com/color-palette/95969
        background_color = "#a2d6ec"
        
         # Insert objects to the UI
        label = tk.Label(self.master, text='Tic-Tac-Toe')
        label.config(font=("times", 30), bg = background_color)
        label.grid(row=0, columnspan=4, ipadx=40, ipady=20)
    
        infoMessageLabel = tk.Label(self.master, text='', textvariable= self.errorMessageVar, fg='red')
        infoMessageLabel.config(font=("Goudy Old Style", 13), bg = background_color)
        infoMessageLabel.grid(row=1, columnspan=4)
    
        label = tk.Label(self.master, text='Select Rationality:')
        label.config(font=("Goudy Old Style", 16), bg = background_color)
        label.grid(row=2, columnspan=4, ipadx=40, ipady=0)
    
        # radio button to set rationality level to 'Level 0'
        rBtnRandom = tk.Radiobutton(self.master, text = "Level 0 (Random)", variable = self.rationalityVar, value = 1)
        rBtnRandom.config(bg = background_color, font=("Goudy Old Style", 12))
        rBtnRandom.grid(row=3, columnspan=4, ipadx=40, ipady=0)
    
        # radio button to set rationality level to 'Level 1'
        rBtnHard = tk.Radiobutton(self.master, text = "Level 1 (Hard-coded)", variable = self.rationalityVar, value = 2)
        rBtnHard.config(bg = background_color, font=("Goudy Old Style", 12))
        rBtnHard.grid(row=4, columnspan=4, ipadx=0, ipady=0)
    
        # radio button to set rationality level to 'Level 2'
        rBtnSearch = tk.Radiobutton(self.master, text = "Level 2 (Minimax)", variable = self.rationalityVar, value = 3)
        rBtnSearch.config(bg = background_color, font=("Goudy Old Style", 12))
        rBtnSearch.grid(row=5, columnspan=4, ipadx=0, ipady=0)
    
        # radio button to set rationality level to 'Level 3'
        rBtnSearch = tk.Radiobutton(self.master, text = "Level 3 (Alphabeta Prunning)", variable = self.rationalityVar, value = 4)
        rBtnSearch.config(bg = background_color, font=("Goudy Old Style", 12))
        rBtnSearch.grid(row=6, columnspan=4, ipadx=0, ipady=0)
        
        btnAccept = tk.Button(self.master, text = "Start", command = self.choice)
        btnAccept.config(font=("Goudy Old Style", 12))
        btnAccept.grid(row=8, columnspan =4, ipadx = 10, pady=(20, 0)) 
        
    # function for button to decide rationality level for next screen
    def choice(self):
        rationality = self.rationalityVar.get()

        # display an information message to notify the user to select
        #   a rationality level
        if rationality == 0:
            self.errorMessageVar.set('Select a rationality level!')
        # otherwise, open game window with selected rationality level
        else:
            title = 'Tic Tac Toe '
            if rationality == 1: title += '- Random'
            elif rationality == 2: title += '- Hard coded'
            elif rationality == 3: title += '- Minimax'
            elif rationality == 4: title += '- Alphabeta Pruning'

            # hide root window
            root.withdraw()
            
            self.newWindow = tk.Toplevel()
            # bind event when the close button of the window is used, not when 
            #   when the 'Quit' button is used
            # https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
            self.newWindow.protocol("WM_DELETE_WINDOW", self.closed_window_callback)
            self.newWindow.title(title)
            self.app = Game(self.master, self.newWindow, rationality)
            

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

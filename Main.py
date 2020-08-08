from GameWindow import Game
import tkinter as tk

class Main:
    
    def __init__(self, master):

        def choice():
            value = var.get()
            if value == 0:
                message_label.config(text='Select a rationality level!')
            else:
                self.master.withdraw()
                self.newWindow = tk.Toplevel(self.master)
                self.app = Game(self.newWindow, value)
        
        def sel():
            message_label.config(text='')

        self.master = master
        #self.frame = tk.Frame(self.master)
        self.master.title("Tic Tac Toe")

        self.master.minsize(width = 200, height = 320)
        self.master.resizable(width = False, height = False)
        var = tk.IntVar()

#Insert objects to the UI

        label = tk.Label(self.master, text='Tic Tac Toe')
        label.config(font=("Adobe Song Std L", 30))
        label.grid(row=0, columnspan=4, ipadx=40, ipady=20)

        message_label = tk.Label(self.master, text='', fg='red')
        message_label.config(font=("Goudy Old Style", 13))
        message_label.grid(row=1, columnspan=4)

        label = tk.Label(self.master, text='Select Rationality:')
        label.config(font=("Goudy Old Style", 16))
        label.grid(row=2, columnspan=4, ipadx=40, ipady=10)

        rBtnRandom = tk.Radiobutton(self.master, text = "Level 0 (Random)", variable = var, value = 1, command = sel)
        rBtnRandom.grid(row=3, columnspan=4, ipadx=40, ipady=0)

        rBtnHard = tk.Radiobutton(self.master, text = "Level 1 (Hard-coded)", variable = var, value = 2, command = sel)
        rBtnHard.grid(row=4, columnspan=4, ipadx=0, ipady=0)

        rBtnSearch = tk.Radiobutton(self.master, text = "Level 2 (Search strategy)", variable = var, value = 3, command = sel)
        rBtnSearch.grid(row=5, columnspan=4, ipadx=0, ipady=0)

        btnAccept = tk.Button(self.master, text = "Accept", command = choice)
        btnAccept.grid(row=7, columnspan =4, ipadx = 10, pady=(20, 0))

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

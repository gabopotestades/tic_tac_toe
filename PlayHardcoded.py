from random import choice

#This function is for Level 1

class HardcodedStrategy:

    def __init__(self, tiles_history, available_moves, rows, columns, first_turn):
        self.rows = rows
        self.columns = columns
        self.first_turn = first_turn
        self.tiles_history = tiles_history
        self.available_moves = available_moves

    def hardCodedMove(self):

        if self.tiles_history[1][1] == '': return (1,1)

        best_move = None

        for item in self.available_moves:

            row = item[0]
            column = item[1]
            
            self.tiles_history[row][column] = 'O'

            #Check if AI will win
            if self.checkWinner('O'):
                self.tiles_history[row][column] = ''
                best_move = (row, column)
                break

            self.tiles_history[row][column] = 'X'

            #Check if Player will win
            if self.checkWinner('X') and best_move == None:
                best_move = (row, column)
        
            self.tiles_history[row][column] = ''

        
        if best_move == None: 

            if self.first_turn == 'O':
                #3rd turn
                if len(self.available_moves) == 7:
                    if self.tiles_history[1][2] == 'X': best_move = (2,0)
                    elif self.tiles_history[1][0] == 'X': best_move = (2,2)
                    elif self.tiles_history[0][1] == 'X': best_move = (2,2)
                    elif self.tiles_history[2][1] == 'X': best_move = (0,0)

            elif self.first_turn == 'X':
                
                #If X entered at the center and O is second turn
                if len(self.available_moves) == 8:
                    #Select random corner
                    best_move = choice([(0,2), (2,0), (0,0), (2,2) ]) 
                
                #If X entered first move not in center and corner then second move is corner
                if len(self.available_moves) == 6:
                    if self.tiles_history[1][2] == 'X':
                        if self.tiles_history[0][0] == 'X':
                            best_move = (0,2)
                        elif self.tiles_history[2][0] == 'X':
                            best_move = (2,2)
                    elif self.tiles_history[1][0] == 'X':
                        if self.tiles_history[0][2] == 'X':
                            best_move = (0,0)
                        elif self.tiles_history[2][2] == 'X':
                            best_move = (2,0)

        #If no best move select random (low chance)
        if best_move == None: best_move = choice(self.available_moves)

        return best_move

    def checkWinner(self, identifier):
        #Horizontal Check
        for i in range(self.rows):
            if self.tiles_history[i][0] == self.tiles_history[i][1] == self.tiles_history[i][2] == identifier:
                return True
        
        #Vertical Check
        for i in range(self.columns):
            if self.tiles_history[0][i] == self.tiles_history[1][i] == self.tiles_history[2][i] == identifier:
                return True

        #Diagonal Check
        if ((self.tiles_history[0][0] == self.tiles_history[1][1] == self.tiles_history[2][2] == identifier) or 
           (self.tiles_history[0][2] == self.tiles_history[1][1] == self.tiles_history[2][0] == identifier) ):
            return True
        
        #Return false if no one wins in current config
        return False
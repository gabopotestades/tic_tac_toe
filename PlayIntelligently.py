from math import inf

class IntelligentStrategy:

    def __init__(self, tiles_history, avail_moves, rows, columns):
        self.tiles_history = tiles_history
        self.avail_moves = avail_moves
        self.rows = rows
        self.columns = columns

    def bestMove(self):

        if self.avail_moves == 9: return (0,0)

        bestScore = -inf
        move = ()

        for i in range(self.rows):
            for j in range(self.columns):
                if self.tiles_history[i][j] == '':
                    self.tiles_history[i][j]  = 'O'
                    self.avail_moves -= 1
                    score = self.miniMax(0, False)
                    self.avail_moves += 1
                    self.tiles_history[i][j] = ''

                    if score > bestScore:
                        bestScore = score
                        move = (i,j)
        
        return move

    def miniMax(self, depth, isMaximizing):
        score_lookup = {'X': -1, 'O': 1, 'draw': 0}
        result = self.checkWinner()

        if result != None: return score_lookup[result]

        if isMaximizing:

            maximizing_BestScore = -inf

            for i in range(self.rows):
                for j in range(self.columns):
                    if self.tiles_history[i][j] == '':
                        self.tiles_history[i][j]  = 'O'
                        self.avail_moves -= 1
                        score = self.miniMax(depth + 1, False)
                        self.avail_moves += 1
                        self.tiles_history[i][j] = ''
                        maximizing_BestScore = max(score, maximizing_BestScore)
            
            return maximizing_BestScore

        else:

            minimizing_BestScore = inf

            for i in range(self.rows):
                for j in range(self.columns):
                    if self.tiles_history[i][j] == '':
                        self.tiles_history[i][j]  = 'X'
                        self.avail_moves -= 1
                        score = self.miniMax(depth + 1, True)
                        self.avail_moves += 1
                        self.tiles_history[i][j] = ''
                        minimizing_BestScore = min(score, minimizing_BestScore)
            
            return minimizing_BestScore

    def checkWinner(self):

        if self.avail_moves == 0 : return 'draw'

        #Horizontal Check
        for i in range(self.rows):
            if self.tiles_history[i][0] == self.tiles_history[i][1] == self.tiles_history[i][2] != '':
                return self.tiles_history[i][0]
        
        #Vertical Check
        for i in range(self.columns):
            if self.tiles_history[0][i] == self.tiles_history[1][i] == self.tiles_history[2][i] != '':
                return self.tiles_history[0][i]

        #Diagonal Check
        if ((self.tiles_history[0][0] == self.tiles_history[1][1] == self.tiles_history[2][2] != '') or 
           (self.tiles_history[0][2] == self.tiles_history[1][1] == self.tiles_history[2][0] != '') ):
            return self.tiles_history[1][1]
        
        

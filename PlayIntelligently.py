from math import inf

class IntelligentStrategy:

    def __init__(self, tiles_history, avail_moves, rows, columns):
        self.tiles_history = tiles_history
        self.avail_moves = avail_moves
        self.rows = rows
        self.columns = columns

    def bestMove(self, rationality):

        #To skip first move since it's always (0,0) if O is first
        #if self.avail_moves == 9: return (0,0)

        bestScore = -inf
        move = ()

        #Instantiate root node for Minimax
        for i in range(self.rows):
            for j in range(self.columns):
                if self.tiles_history[i][j] == '':
                    self.tiles_history[i][j]  = 'O'
                    self.avail_moves -= 1
                    if rationality == 3:
                        score = self.miniMax(0, False)
                    else:
                        score = self.alphaBetaPrunning(0, -inf, inf, False)
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

        #If bool is true, pick move with chance to win
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

        #If bool is false, pick move with chance to not lose
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

    def alphaBetaPrunning(self, depth, alpha, beta, isMaximizing):
        score_lookup = {'X': -1, 'O': 1, 'draw': 0}
        result = self.checkWinner()

        if result != None: return score_lookup[result]

        #If bool is true, pick move with chance to win
        if isMaximizing:

            maximizing_BestScore = -inf

            for i in range(self.rows):
                for j in range(self.columns):
                    if self.tiles_history[i][j] == '':
                        self.tiles_history[i][j]  = 'O'
                        self.avail_moves -= 1 
                        # o_score = self.evaluationHeuristic('O')
                        # x_score = self.evaluationHeuristic('X')
                        # eval_score = o_score - x_score
                        eval_score = self.evaluationHeuristic('O') - self.evaluationHeuristic('X')
                        score = self.alphaBetaPrunning(depth + 1, alpha, beta, False) + eval_score
                        self.avail_moves += 1
                        self.tiles_history[i][j] = ''
                        maximizing_BestScore = max(score, maximizing_BestScore)
                        alpha = max(alpha, score)
                        #if beta <= alpha:
                            #break
                #if beta <= alpha:
                    #break
            
            return maximizing_BestScore

        #If bool is false, pick move with chance to not lose
        else:

            minimizing_BestScore = inf

            for i in range(self.rows):
                for j in range(self.columns):
                    if self.tiles_history[i][j] == '':
                        self.tiles_history[i][j]  = 'X'
                        self.avail_moves -= 1
                        # o_score = self.evaluationHeuristic('O')
                        # x_score = self.evaluationHeuristic('X')
                        # eval_score = x_score - o_score
                        eval_score = self.evaluationHeuristic('X') - self.evaluationHeuristic('O')
                        score = self.alphaBetaPrunning(depth + 1, alpha, beta, True) + eval_score
                        self.avail_moves += 1
                        self.tiles_history[i][j] = ''
                        minimizing_BestScore = min(score, minimizing_BestScore)
                        beta = min(beta, score)
                        #if beta <= alpha:
                            #break
                #if beta <= alpha:
                    #break
            
            return minimizing_BestScore  

    def checkWinner(self):

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

        #Check if no possible moves left 
        if self.avail_moves == 0 : return 'draw'

    def evaluationHeuristic(self, player):
        
        score = 0

        #Horizontal Check
        for i in range(self.rows):
            if convertEmpty(self.tiles_history[i][0], player) == \
               convertEmpty(self.tiles_history[i][1], player) == \
               convertEmpty(self.tiles_history[i][2], player) == player:
                score +=1
        
        #Vertical Check
        for i in range(self.columns):
            if convertEmpty(self.tiles_history[0][i], player) == \
               convertEmpty(self.tiles_history[1][i], player) == \
               convertEmpty(self.tiles_history[2][i], player) == player:
                score += 1

        #Diagonal Check
        if convertEmpty(self.tiles_history[0][0], player) == \
           convertEmpty(self.tiles_history[1][1], player) == \
           convertEmpty(self.tiles_history[2][2], player) == player:
            score += 1
        if convertEmpty(self.tiles_history[0][2], player) == \
           convertEmpty(self.tiles_history[1][1], player) == \
           convertEmpty(self.tiles_history[2][0], player) == player:
            score += 1

        return score

#Convert empty tile to a player for simulation
def convertEmpty(tile, player):
    return player if tile == '' else tile

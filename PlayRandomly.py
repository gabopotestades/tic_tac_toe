from random import choice

class RandomStrategy:

    def __init__(self, available_moves):
        self.available_moves = available_moves
    
    def random_move(self):
        return choice(self.available_moves)
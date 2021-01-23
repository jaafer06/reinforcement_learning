#%%
import numpy as np
from game_logic import *

class Sarsa:
    def __init__(self, game: Game, state_lenth, num_actions, lamda=0.5, decay_rate=0.5, epsilone=0.5):
        dt = np.dtype([('Q',float), ('E',float)])
        self.Q_table = np.zeros((*state_lenth, num_actions), dtype=dt)
        self.Q_table[:, :] = 0
        self.game = game

    def update(self, k):
        for _ in range(k):
            game.reset()
            self.Q_table["E"] = 0
            
    def get_state(self):
        return (self.game)


q_l = Sarsa([10, 10, 10, 10], 5)
print(q_l.Q_table["E"])
from reinforcement_learning import *
from collections import defaultdict
import numpy as np
import game_logic as gl
import pickle
import sys

sarsa = None
game_logic = None

# "lamda": 0.01, "decay_rate": 0.95, "epsilone": 0.5, "learning_rate": 0.3
params = {
    "lamda": 0.01, "decay_rate": 0.9, "epsilone": 0.95, "learning_rate": 0.01
}

print(sys.argv)

if len(sys.argv) == 3 and sys.argv[1] == "resume":
    sarsa = Sarsa.load(sys.argv[-1])
else:
    game_logic = gl.Game(10, 10, position=np.array([2, 8]), enemy_positions=np.array([[5, 5], [ 1, 3], [7, 4], [0, 8]]))
    # sarsa = Sarsa(game_logic, [10, 10, 10, 10], 4, **params)
    sarsa = Sarsa(game_logic, [20, 8, 8, 8, 8, 2], 4, **params)



#%%

#%%


#%%
print_every = 100
running_loss = 0
running_episode_length = 0
running_won = 1
running_won_episode_length = 0
for k in range(1, 30000):
    episode_length, lost = sarsa.episode_update()
    running_episode_length += episode_length
    running_loss += lost
    running_won += not lost
    running_won_episode_length += episode_length if not lost else 0
    if k % print_every == 0:
        print("loss", running_loss/print_every)
        print("length", running_episode_length/print_every)
        print("length won", running_won_episode_length/running_won)
        print("epsilone", sarsa.epsilone)
        print("progress", k/30000)

        print("----")

        running_loss = 0
        running_episode_length = 0
        running_won_episode_length = 0
        running_won = 1


#%%
sarsa.save()
#%%
import numpy as np
import game_logic as gl
import pickle

class Sarsa:
    def __init__(self, game: gl.Game, state_lenth, num_actions, lamda=0.5, decay_rate=0.5, epsilone=0.5, learning_rate=0.5):
        dt = np.dtype([('Q',float), ('E',float)])
        self.Q_table = np.zeros((*state_lenth, num_actions), dtype=dt)
        self.Q_table[:, :] = 0
        self.game = game
        self.epsilone = epsilone
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate
        self.lamda = lamda
        self.num_actions = num_actions
        self.step = 0
        # self.Q_table["Q"] = np.random.sample(self.Q_table["Q"].shape)
     
    # def get_state(self):
    #     return (*self.game.player_position, *self.game.enemy_positions[0])

    def get_state(self):
        direction_vectors = self.game.enemy_positions-self.game.player_position
        l1_exit = np.linalg.norm(self.game.player_position - self.game.exit_positions[0], ord=1).astype(int)
        
        l1_norms = np.linalg.norm(direction_vectors, ord=np.inf, axis=1)

        mode = 0
        if np.all(l1_norms > 1):
            return (l1_exit, *np.zeros(self.game.enemy_positions.shape[0], dtype=int), 0)
    

        angles = np.angle(direction_vectors[:, 0] + np.complex(0,1)*direction_vectors[:, 1])
        angles[angles<0] += (np.pi * 2)
        angles = (angles//(np.pi/4)).astype(int)

        return (0, *angles, 1)


    def episode_update(self):
        self.game.reset()
        # print(self.game.player_position)
        self.Q_table["E"] = 0

        # print(self.game.exit_positions)
        state = self.get_state()
        terminal_state = False
        action = self.chose_action(state)
        episode_length = 0
        # actions = [action]
        while(not terminal_state):
            won, enemy_hit = self.game.move(action)
            terminal_state = won or enemy_hit
            reward = self.get_reward(won, enemy_hit)

            next_state = self.get_state()
            next_action = self.chose_action(next_state)
            delta = reward + self.decay_rate * self.Q_table[(*next_state, next_action)]["Q"] - self.Q_table[(*state, action)]["Q"]
            self.Q_table[(*state, action)]["E"] = self.Q_table[(*state, action)]["E"] + 1
            self.update_q_e(delta)
            state = next_state
            action = next_action

            episode_length = 1 + episode_length
            # actions.append(action)
            # if won:
            #     print(self.game.exit_positions)
            #     print(self.game.player_position)
            #     print(episode_length)
            #     print(actions)

        self.step += 1
        self.epsilone = self.linear_decay(40000)/4
        return episode_length, enemy_hit

    def update_q_e(self, delta):
        mask = self.Q_table["E"] != 0
        self.Q_table["Q"][mask] += (delta * self.learning_rate * self.Q_table["E"][mask])

        self.Q_table["E"][mask] = self.Q_table["E"][mask] * self.lamda * self.decay_rate

    def chose_action(self, state):
        q_values = self.Q_table[state]["Q"]
        max_q_action_index = np.argmax(self.Q_table[state]["Q"])
        greedy = np.random.binomial(1, 1-self.epsilone) == 1
        if greedy:
            return int(max_q_action_index)
        else:
            actions = list(range(0, max_q_action_index)) + list(range(max_q_action_index+1, self.num_actions))
            return int(np.random.choice(actions))


    def get_reward(self, won, enemy_hit):
        # distance_score = -np.linalg.norm(self.game.exit_positions[0]-self.game.player_position, ord= np.inf)
        if won:
            return 100
        elif enemy_hit:
            return -10
        else:
            return -1

    def get_Q_max_action(self, game):
        my_game = self.game
        self.game = game
        state = self.get_state()
        self.game = my_game
        return np.argmax(self.Q_table[state]["Q"])

    def linear_decay(self, max_step_until_zero):
        return max(0, 1 - self.step * (1/max_step_until_zero))

    def save(self):
        pickle.dump(self, open("sarsa.p", "wb"))

    @staticmethod
    def load(name):
        return pickle.load(open(name, 'rb'))

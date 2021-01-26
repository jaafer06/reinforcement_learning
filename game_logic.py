import numpy as np
from collections import defaultdict



class Bots_logic1:
    def __init__(self, positions, max_coordinates):
        self.positions = positions
        self.directions = None
        self.chose_random_directions()
        self.index = 0
        self.max_coordinates = max_coordinates

    def chose_random_directions(self):
        self.directions = [Game.actions_to_directions[np.random.choice(Game.actions)] for _ in range(self.positions.shape[0])]

    def move(self):
        # if self.index == 2:
        #     self.index = 0
        #     self.chose_random_directions()

        # self.index += 1
        self.chose_random_directions()
        np.add(self.positions, self.directions, out=self.positions)

        mask = self.positions < 0
        if np.any(mask):
            self.positions[mask] = 0
        mask = self.positions > self.max_coordinates
        if np.any(mask):
            m = np.repeat([self.max_coordinates], self.positions.shape[0], axis=0)
            self.positions[mask] = m[mask]

class Game:
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3
    actions = [DOWN, RIGHT, UP, LEFT]
    actions_to_directions = {DOWN: np.array([0, 1]), RIGHT: np.array([1, 0]), UP: np.array([0, -1]), LEFT: np.array([-1, 0])}

    def __init__(self, width, height, position=None, exit_positions=None, enemy_positions=None):
        self.exit_positions = exit_positions if exit_positions is not None else np.array([[width - 1, 0]])
        self.max_coordinates = np.array([width - 1, height - 1])
        
        self.player_position = position if position is not None else np.array([0, height-1])
        self.P = defaultdict(list)

        self.enemy_positions = enemy_positions if enemy_positions is not None else np.array([[width-3, height -3]])
        self.bot_logic = Bots_logic1(self.enemy_positions, self.max_coordinates)

        self._initial_player_positon = np.copy(self.player_position)
        self._initial_enemy_positions = np.copy(self.enemy_positions[:])
        self._initial_exit_positions = np.copy(self.exit_positions[:])


    def reset(self):
        self.player_position[:] = self._initial_player_positon
        self.enemy_positions[:] = self._initial_enemy_positions
        self.exit_positions[:] = self._initial_exit_positions


    def move(self, action):
        direction = Game.actions_to_directions[action]
        np.add(self.player_position, direction, out=self.player_position)
        mask = self.player_position < 0
        if np.any(mask):
            self.player_position[mask] = 0
        mask = self.player_position > self.max_coordinates
        if np.any(mask):
            self.player_position[mask] = self.max_coordinates[mask]


        self.bot_logic.move()

        enemy_hit = np.any(np.all(self.player_position == self.enemy_positions, axis=1))
        game_won = np.any(np.all(self.player_position == self.exit_positions, axis=1))
        
        return  game_won, enemy_hit

if __name__ == "__main__":
    game = Game(10, 10, enemy_positions=np.array([[8, 1], [7, 7]]))
    for i in range(20):
        game.move(Game.RIGHT)
        game.move(Game.UP)
        print(game.player_position)
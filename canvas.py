import pygame
import pygame_gui
import numpy as np
import game_logic as gl
from ui_asssets import *
from reinforcement_learning_algorithms import *
import pickle

pygame.init()

window_size = np.array([1200, 800])
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(window_size)
manager = pygame_gui.UIManager(window_size, 'data/themes/quick_theme.json')

screen = pygame.Surface(window_size)
screen.fill(manager.ui_theme.get_colour('dark_bg'))

# cell = Cell(screen, (100, 100, 50, 50), "P")
# cell.render()
# game_logic = gl.Game(10, 10, enemy_positions=np.array([[7, 2], [5, 5], [9, 9], [5, 5], [0, 5]]))
# game_logic = gl.Game(10, 10, enemy_positions=np.array([[7, 2], [5, 5], [9, 9], [5, 5], [0, 5]]))
game_logic = gl.Game(10, 10, position=np.array([0, 8]), enemy_positions=np.array([[5, 5]]))

game = Game(screen, np.zeros((10, 10)), (60, 60), game_logic.player_position, game_logic.enemy_positions, game_logic.exit_positions)
game.render(game_logic.player_position, game_logic.enemy_positions, game_logic.exit_positions)
with open('gli3.p', 'rb') as f:
    glie = pickle.load(f)

button_size = np.array([150, 40])
first_button_position = [window_size[0] - button_size[0] - 50, 200]

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(first_button_position, button_size),
                                            text='Hello',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True

def get_state(game_logic):
    return (*game_logic.player_position, *np.ndarray.flatten(game_logic.enemy_positions))

    direction_vector = game_logic.player_position - game_logic.enemy_positions[0]
    position = game_logic.player_position
    l1_norm = np.linalg.norm(direction_vector, ord=np.inf)
    if l1_norm >2:
        direction_vector[:] = 10
    else:
        position = (-1, -1) 
    return (*position, np.floor(l1_norm), *direction_vector)

def update():
    try:
        s = get_state(game_logic)
        game_logic.move(glie.get_action(s))
        game.render(game_logic.player_position, game_logic.enemy_positions, game_logic.exit_positions)
    except:
        game_logic.reset()

while is_running:
    time_delta = clock.tick(10)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_element == hello_button):
            game_logic.reset()
            print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    update()
    window_surface.blit(screen, (0, 0))

    manager.draw_ui(window_surface)

    pygame.display.update()
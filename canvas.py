import pygame
import pygame_gui
import numpy as np
import game_logic as gl
from ui_asssets import *
from reinforcement_learning import *
import pickle

pygame.init()
actions =[2, 1, 2, 1, 1, 2, 1, 2, 1, 0]
window_size = np.array([1200, 800])
game_running = False
display_Q = False
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(window_size)
manager = pygame_gui.UIManager(window_size, 'data/themes/quick_theme.json')

screen = pygame.Surface(window_size)
screen.fill(manager.ui_theme.get_colour('dark_bg'))

# cell = Cell(screen, (100, 100, 50, 50), "P")
# cell.render()
# game_logic = gl.Game(10, 10, enemy_positions=np.array([[7, 2], [5, 5], [9, 9], [5, 5], [0, 5]]))
# game_logic = gl.Game(10, 10, enemy_positions=np.array([[7, 2], [5, 5], [9, 9], [5, 5], [0, 5]]))
sarsa = Sarsa.load("sarsa.p")
game_logic = sarsa.game
game_logic.reset()
game = Game(screen, np.zeros((10, 10)), (60, 60), game_logic.player_position, game_logic.enemy_positions, game_logic.exit_positions)
game.render(game_logic.player_position, game_logic.enemy_positions, game_logic.exit_positions)

button_size = np.array([150, 40])
first_button_position = [window_size[0] - button_size[0] - 50, 200]
button_offset = np.array([0, button_size[1] + 20])
play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(first_button_position, button_size),
                                            text='play/stop',
                                            manager=manager)

step_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(button_offset + first_button_position, button_size),
                                            text='step',
                                            manager=manager)

display_Q_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(2*button_offset + first_button_position, button_size),
                                            text='display Q',
                                            manager=manager)

reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(3*button_offset+first_button_position, button_size),
                                            text='reset',
                                            manager=manager)


clock = pygame.time.Clock()
is_running = True


def update():
    try:
        if not game_running:
            return
        action = sarsa.get_Q_max_action(game_logic)
        sarsa_game = sarsa.game
        sarsa.game = game_logic
        print(sarsa.get_state())
        sarsa.game = sarsa_game
        # action = actions.pop(0)
        game_logic.move(action)
        game.render(game_logic.player_position, game_logic.enemy_positions, game_logic.exit_positions)
    except:
        game_logic.reset()

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_element == play_button):
            game_running = not game_running

        elif (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and
            event.ui_element == reset_button):
            game_logic.reset()
            game_running = False
            game.render(game_logic.player_position, game_logic.enemy_positions, game_logic.exit_positions)


        elif (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and
            event.ui_element == step_button):
            game_running = True
            update()
            game_running = False

        manager.process_events(event)

    manager.update(time_delta)

    update()
    window_surface.blit(screen, (0, 0))

    manager.draw_ui(window_surface)

    pygame.display.update()
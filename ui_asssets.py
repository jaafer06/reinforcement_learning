import pygame
import pygame_gui
import numpy as np


arrow = pygame.transform.scale(pygame.image.load("img/arrow2.png"), [50, 50])
arrow_rot = pygame.transform.rotate(arrow, 90)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

class Cell:
    def __init__(self, surface, rect, content="", arrow=None):
        self.surface = surface
        self.rect = rect
        self.position = np.array([rect[0], rect[1]])
        self.size = np.array([rect[2], rect[3]])
        self.textsurface = myfont.render(content, False, (0, 0, 0))
        
    
    def render(self, texture=None):
        pygame.draw.rect(self.surface, "white", self.rect)
        if texture is not None:
            self.surface.blit(texture, (self.position) + self.size/3)
        # self.surface.blit(arrow, (0, 0))
        # self.surface.blit(arrow_rot, (200, 200))

class Game:
    player_texture = myfont.render("P", False, (0, 0, 0))
    enemy_texture = myfont.render("E", False, (0, 0, 0))
    exit_texture = myfont.render("exit", False, (0, 0, 0))

    def __init__(self, surface, grid, cell_size, player_position, enemies_positions, exits_positons,offset=(100, 100)):
        self.surface = surface
        self.cell_size = cell_size
        self.grid = grid
        self.cell_grid = []
        self.offset = offset
        x_max, y_max = self.grid.shape
        for x in range(x_max):
            new_row = []
            self.cell_grid.append(new_row)
            for y in range(y_max):
                cell = Cell(surface, (self.offset[0] + x*cell_size[0] + 5 *x, self.offset[1] + y*cell_size[1] + 5*y, *cell_size))
                cell.render()
                new_row.append(cell)
        

    def render(self, player_position, enemies_positions, exits_positons):
        for row in self.cell_grid:
            for cell in row:
                cell.render()
        self.cell_grid[player_position[0]][player_position[1]].render(Game.player_texture)
        for enemy_position in enemies_positions:
            self.cell_grid[enemy_position[0]][enemy_position[1]].render(Game.enemy_texture)
        for exit_position in exits_positons:
            self.cell_grid[exit_position[0]][exit_position[1]].render(Game.exit_texture)




        

        
    # def render(self):
    #     x_max, y_max = self.gid.shape
    #     for x in x_max:
    #         for y in y_max:


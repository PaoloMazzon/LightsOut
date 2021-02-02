# Author: Paolo Mazzon 2021
# License: CC0 - public domain

import pygame
from random import randint
from math import floor
from io import BytesIO

red_button_png = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x0A, 0x08, 0x06, 0x00, 0x00, 0x00, 0x8D, 0x32, 0xCF, 0xBD, 0x00, 0x00, 0x00, 0x36, 0x49, 0x44, 0x41, 0x54, 0x18, 0x95, 0x63, 0x64, 0x60, 0x60, 0xF8, 0xCF, 0x40, 0x04, 0x60, 0x61, 0x60, 0x60, 0x60, 0xF8, 0xFF, 0x1F, 0x49, 0x2D, 0x23, 0x23, 0x86, 0x22, 0x46, 0x98, 0x42, 0x5C, 0x0A, 0x90, 0x01, 0x13, 0x31, 0xD6, 0x22, 0x14, 0x12, 0x30, 0x8D, 0x0C, 0x13, 0x07, 0x44, 0x21, 0x23, 0x03, 0x91, 0x01, 0x0E, 0x00, 0x15, 0xA8, 0x05, 0x19, 0x22, 0xF2, 0x49, 0xC4, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]
blue_button_png = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x0A, 0x08, 0x06, 0x00, 0x00, 0x00, 0x8D, 0x32, 0xCF, 0xBD, 0x00, 0x00, 0x00, 0x38, 0x49, 0x44, 0x41, 0x54, 0x18, 0x95, 0x63, 0x64, 0x60, 0x60, 0xF8, 0xCF, 0x40, 0x04, 0x60, 0x61, 0x60, 0x60, 0x60, 0xF8, 0xFF, 0x1F, 0xA1, 0x96, 0x31, 0x76, 0x16, 0xA6, 0xAA, 0x25, 0xE9, 0x10, 0x85, 0x38, 0x15, 0x20, 0x01, 0x26, 0x62, 0xAC, 0x85, 0x2B, 0x24, 0x64, 0x1A, 0xE9, 0x26, 0x0E, 0x8C, 0x42, 0x46, 0x06, 0x22, 0x03, 0x1C, 0x00, 0xD5, 0x20, 0x09, 0x05, 0xA1, 0x38, 0x5B, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]

png_size = (10, 10)
png_width, png_height = png_size
grid_size = (3, 3)
grid_width, grid_height = grid_size
screen_scale = 15
screen_size = (grid_width * screen_scale * png_width, grid_height * screen_scale * png_width)
screen_width, screen_height = screen_size

def random_grid():
    grid = []
    for i in range(grid_height):
        temp = []
        for j in range(grid_width):
            temp += [randint(0, 1)]
        grid += [temp]
    return grid
 
def toggle_pos(grid, mouse):
    x, y = mouse
    x = int(x)
    y = int(y)
    if 0 <= x < grid_width and 0 <= y < grid_height:
        if grid[y][x] == 1:
            grid[y][x] = 0
        else:
            grid[y][x] = 1
    return grid
 
def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    buffer = pygame.Surface((png_width * grid_width, png_height * grid_height))
    ret = False # if true the game quits
    grid = random_grid()
    pygame.display.set_caption("Space to randomize board, E to toggle edit mode")
    edit = False # edit raw grid mode
    f = BytesIO(bytes(red_button_png))
    red_button_surface = pygame.image.load(f, "png")
    f = BytesIO(bytes(blue_button_png))
    blue_button_surface = pygame.image.load(f, "png")
 
    while not ret:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ret = True
            if event.type == pygame.MOUSEBUTTONDOWN: click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: grid = random_grid()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e: edit = not edit
 
        # check user input
        if pygame.mouse.get_pressed()[0] and click:
            x, y = pygame.mouse.get_pos()
            x = floor(x / (screen_width / grid_width))
            y = floor(y / (screen_height / grid_height))
            toggle_pos(grid, (x, y))
            if not edit:
                toggle_pos(grid, (x + 1, y))
                toggle_pos(grid, (x, y + 1))
                toggle_pos(grid, (x, y - 1))
                toggle_pos(grid, (x - 1, y))
        
        win = 0
        for i in grid: 
            if not 1 in i: win += 1
        if win == len(grid) and not edit:
            pygame.display.set_caption("You win! Space to randomize board")
        elif edit:
            pygame.display.set_caption("Edit mode, Space to randomize board and E to exit edit mode")
        else:
            pygame.display.set_caption("Space to randomize board, E to toggle edit mode")
 
        # fill out texture
        for i in range(grid_height):
            for j in range(grid_width):
                if (grid[i][j] == 0):
                    buffer.blit(red_button_surface, (j * png_width, i * png_height))
                else:
                    buffer.blit(blue_button_surface, (j * png_width, i * png_height))
 
        # draw scaled screen
        scaled_screen = pygame.transform.scale(buffer, screen_size)
        screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()
 
if __name__ == "__main__":
    main()
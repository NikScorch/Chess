#!/bin/python3
#       _
#   ___| |__   ___  ___ ___
#  / __| '_ \ / _ \/ __/ __|
# | (__| | | |  __/\__ \__ \
#  \___|_| |_|\___||___/___/
#   ____ _
#  / ___| |__   ___  ___ ___
# | |   | '_ \ / _ \/ __/ __|
# | |___| | | |  __/\__ \__ \
#  \____|_| |_|\___||___/___/
#   ____ _   _ _____ ____ ____
#  / ___| | | | ____/ ___/ ___|
# | |   | |_| |  _| \___ \___ \
# | |___|  _  | |___ ___) |__) |
#  \____|_| |_|_____|____/____/
#

import pygame

def draw_board():
    boxwidth = screen.get_width() / 8
    box_colour = [(0,0,0), (255,255,255)]
    box_count = 0
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, box_colour[box_count%2], (j*boxwidth,i*boxwidth,boxwidth,boxwidth))
            box_count += 1
        box_count += 1

class ChessPiece(pygame.sprite.sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, piece)
        self.image, self.rect = load_image("pieces/{}.svg", -1)

board = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []]

pygame.init()

size = width, height = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

while True:
    # Player Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit



    # Logical Updates
    draw_board()



    # Graphics Rendering
    pygame.display.flip()
    clock.tick(60)
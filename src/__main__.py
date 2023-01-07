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
    box_width = screen.get_width() / 8
    box_colour = [(255,255,255), (0,0,0)]
    box_count = 0
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, box_colour[box_count%2], (j*box_width,i*box_width,box_width,box_width))
            box_count += 1
        box_count += 1

class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, piece_set, piece):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("src/pieces/{}/{}.png".format(piece_set, piece))
        self.image = pygame.transform.scale(self.image, (screen.get_width()/8, screen.get_width()/8)).convert_alpha()
        self.rect = self.image.get_rect()
        

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x, self.rect.y = (pos[0] - self.rect.width/2, pos[1] - self.rect.width/2)
        #self.rect.posXY = pos
        
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

pieces = [
    ChessPiece("cardinal_png", "bq"),
    ChessPiece("cardinal_png", "bk"),
    ChessPiece("cardinal_png", "bp"),
    ChessPiece("cardinal_png", "br"),
    ChessPiece("cardinal_png", "bb"),
    ChessPiece("cardinal_png", "bk"),
    ChessPiece("cardinal_png", "wq"),
    ChessPiece("cardinal_png", "wk"),
    ChessPiece("cardinal_png", "wp"),
    ChessPiece("cardinal_png", "wr"),
    ChessPiece("cardinal_png", "wb"),
    ChessPiece("cardinal_png", "wk"),
]
allsprites = pygame.sprite.RenderPlain((pieces))

while True:
    # Player Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit



    # Logical Updates
    allsprites.update()



    # Graphics Rendering
    draw_board()
    allsprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)
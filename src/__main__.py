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
#
#
# # of moves
# time
# number of times each piece was moveed
# allow pieces to jump over all other pieces???
# - remove a check from legal moves algotithm (TODO)

# posiotion you want ot move to 
# if its viable, check path to square from starting position

# hypothesis/advanced
# change arrangement of hte pieces
# * remove pawns
# * move all pieces/front row forward
# * draught formation for pieces
#
# add saving of progress and resume progress
# autosave? yessss


import pygame
from random import randint
from math import dist
from time import sleep

# These functions convert array coords into Square Names
# e.g. (0,0) --> "a8"
#      "b4"  --> (1,4)
#      (3,6) --> "d2"
def board_to_coord(square):
    convert_table = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7
    }
    return (convert_table[square[0]], 8-int(square[1]))
    
def coord_to_board(coord):
    convert_table = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return convert_table[coord[0]] + str(8-coord[1])

def slope(point1, point2):
    return (point2[1]-point1[1])/(point2[0]-point1[0])


def draw_board():
    box_width = screen.get_width() / 8
    box_colour = [(255,255,255), (0,0,0)]
    box_count = 0
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, box_colour[box_count%2], (j*box_width,i*box_width,box_width,box_width))
            box_count += 1
        box_count += 1
    box_count = 1
    for engraving in range(8):
        # render numbers first
        engrave = board_font.render(str(8-engraving), False, box_colour[box_count%2])
        screen.blit(engrave, (5,100*engraving +5))
        box_count += 1
    box_count =0
    convert_table = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for engraving in range(8):
        # render letters second
        engrave = board_font.render(str(convert_table[engraving]), False, box_colour[box_count%2])
        screen.blit(engrave, (100*engraving +85, 780))
        box_count += 1
    


def find_closest(pieces, mouse_pos):
    closest_piece_str = ""
    closest_piece = ""
    closest_distance = -1
    for piece in pieces:
        mouse_to_piece = dist(mouse_pos, (piece.rect.x+50, piece.rect.y+50))
        if closest_distance == -1:
            closest_distance = mouse_to_piece
            #closest_piece = piece.piece
            closest_piece = piece
        if mouse_to_piece < closest_distance:
            closest_distance = mouse_to_piece
            #closest_piece = piece.colour + piece.piece 
            closest_piece = piece
    if closest_distance > 50:
        return None
    return closest_piece

class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, piece_set, piece, start_pos=None):
        pygame.sprite.Sprite.__init__(self)
        self.piece_set = piece_set
        self.colour = piece[0]
        self.piece = piece[1]
        self.attached = False                   # Picked up with mouse
        self.status = True                      # Alive or Dead/True or False
        self.aggression = False

        self.image = pygame.image.load("src/pieces/{}/{}{}.png".format(self.piece_set, self.colour, self.piece))
        self.image = pygame.transform.scale(self.image, (screen.get_width()/8, screen.get_width()/8)).convert_alpha()
        self.rect = self.image.get_rect()

        if start_pos == None:
            # Random start position
            self.rect.x = randint(0, 7)*100                     # Current X pos
            self.rect.y = randint(0, 7)*100                     # Current Y pos
            self.xy = (self.rect.x//100, self.rect.y//100)      # Where the piece just was
        else:
            # Set start position
            self.xy = board_to_coord(start_pos)
            self.rect.x = self.xy[0]*100
            self.rect.y = self.xy[1]*100

    def update(self):
        if self.attached == True:
            self.aggression = True
            pos = pygame.mouse.get_pos()
            self.rect.x, self.rect.y = (pos[0] - self.rect.width/2, pos[1] - self.rect.width/2)
        elif self.attached == False:
            self.rect.x = (self.rect.x+50)//100*100
            self.rect.y = (self.rect.y+50)//100*100

            if self.check_position((self.rect.x//100, self.rect.y//100)):
                self.xy = (self.rect.x//100, self.rect.y//100)
            else:
                self.rect.x = self.xy[0]*100
                self.rect.y = self.xy[1]*100

            self.promote()  # Check for need to promote
            # Remove enemy piece if aggressive
            if self.aggression:
                # determine enemy
                if self.colour == "w":
                    enemy = black
                elif self.colour == "b":
                    enemy = white
                # Remove piece
                for piece in enemy:
                    if piece.xy == self.xy:
                        piece.remove()
                self.aggression = False
            
    def check_position(self, new_pos):
        if self.xy == new_pos:
            return False

        if self.piece == "p":   # pawn
            if round(dist(self.xy, new_pos), 1) in (1.4,1.0,2.0):
                if self.colour == "w":
                    # if still on the first rank
                    if self.xy[1] == 6:
                        if self.xy[1] - new_pos[1] == 2:
                            return True
                    if self.xy[1] - new_pos[1] == 1:
                        return True
                if self.colour == "b":
                    # if still on the first rank
                    if self.xy[1] == 1:
                        if self.xy[1] - new_pos[1] == -2:
                            return True
                    if self.xy[1] - new_pos[1] == -1:
                        return True

            return False
        if self.piece == "r":   # rook
            if self.xy[0] == new_pos[0] or self.xy[1] == new_pos[1]:
                return True
            else:
                return False
        if self.piece == "b":   # bishop
            if self.xy[0] == new_pos[0] or self.xy[1] == new_pos[1]:
                return False
            if abs(slope(self.xy, new_pos)) == 1.0:
                return True
            else:
                return False
        if self.piece == "n":   # knight
            if round(dist(self.xy, new_pos), 1) == 2.2:
                return True
            else:
                return False
        if self.piece == "k":   # king
            if round(dist(self.xy, new_pos), 1) == 1.4 or round(dist(self.xy, new_pos), 1) == 1.0:
                return True
            else:
                return False
        if self.piece == "q":   # queen
            if self.xy[0] == new_pos[0] or self.xy[1] == new_pos[1]:
                return True
            elif abs(slope(self.xy, new_pos)) == 1.0:
                return True
            else:
                return False
        pass

    def promote(self):
        if self.piece == "p":
            if self.colour == "w" and self.rect.y//100 == 0 or self.colour == "b" and self.rect.y//100 == 7:
                self.piece = "q"
                self.image = pygame.image.load("src/pieces/{}/{}{}.png".format(self.piece_set, self.colour, self.piece))
                self.image = pygame.transform.scale(self.image, (screen.get_width()/8, screen.get_width()/8)).convert_alpha()
    def remove(self):
        if self.piece == "k":
            if self.colour == "w":
                winner[0] = "Black"
            elif self.colour == "b":
                winner[0] = "White"
            
        self.xy = (-100, -100)
        self.rect.x, self.rect.y = self.xy
    


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

chess_set = "cardinal_png"
white = [
    ChessPiece(chess_set, "wp", "a2"),
    ChessPiece(chess_set, "wp", "b2"),
    ChessPiece(chess_set, "wp", "c2"),
    ChessPiece(chess_set, "wp", "d2"),
    ChessPiece(chess_set, "wp", "e2"),
    ChessPiece(chess_set, "wp", "f2"),
    ChessPiece(chess_set, "wp", "g2"),
    ChessPiece(chess_set, "wp", "h2"),
    ChessPiece(chess_set, "wr", "a1"),
    ChessPiece(chess_set, "wn", "b1"),
    ChessPiece(chess_set, "wb", "c1"),
    ChessPiece(chess_set, "wq", "d1"),
    ChessPiece(chess_set, "wk", "e1"),
    ChessPiece(chess_set, "wb", "f1"),
    ChessPiece(chess_set, "wn", "g1"),
    ChessPiece(chess_set, "wr", "h1")
]
black = [
    ChessPiece(chess_set, "bp", "a7"),
    ChessPiece(chess_set, "bp", "b7"),
    ChessPiece(chess_set, "bp", "c7"),
    ChessPiece(chess_set, "bp", "d7"),
    ChessPiece(chess_set, "bp", "e7"),
    ChessPiece(chess_set, "bp", "f7"),
    ChessPiece(chess_set, "bp", "g7"),
    ChessPiece(chess_set, "bp", "h7"),
    ChessPiece(chess_set, "br", "a8"),
    ChessPiece(chess_set, "bn", "b8"),
    ChessPiece(chess_set, "bb", "c8"),
    ChessPiece(chess_set, "bq", "d8"),
    ChessPiece(chess_set, "bk", "e8"),
    ChessPiece(chess_set, "bb", "f8"),
    ChessPiece(chess_set, "bn", "g8"),
    ChessPiece(chess_set, "br", "h8")
]

whitesprites = pygame.sprite.RenderPlain(white)
blacksprites = pygame.sprite.RenderPlain(black)
pieces = [white + black]
allsprites = pygame.sprite.RenderPlain(pieces)

board_font = pygame.font.SysFont("FreeSans", 15, bold=True)

winner = [None] # Set to "Black" or "White" depending winner, set None if undecided

def __main__():
    while True:
        # Player Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                found_piece = find_closest(white + black, mouse_pos)
                if not found_piece == None:
                    found_piece.attached = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                found_piece = find_closest(white + black, mouse_pos)
                if not found_piece == None:
                    found_piece.attached = False
            
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    for piece in white + black:
                        if piece.piece == "p":
                            piece.remove()



        # Logical Updates
        #allsprites.update()
        whitesprites.update()
        blacksprites.update()
        
        #fps_counter = pygame.font.render("FPS:", ())
        fps_counter = board_font.render('FPS: {}'.format(str(round(clock.get_fps(), 1))), False, (150, 50, 50))
        
        if winner[0]:
            winner_text = board_font.render("{} has won!".format(winner[0]), False, (0,255,255))



        # Graphics Rendering
        draw_board()
        allsprites.draw(screen)

        screen.blit(fps_counter, (0,0))
        if winner[0]:
            screen.blit(winner_text, (350,0))


        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    __main__()
#!/usr/bin/python3
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
#
# add references to important pieces of code, ie. their line number (and what it is doing) (mention in the readme?)

import pygame
from random import randint
from math import dist
from time import time
import json

# These functions convert array coords into Square Names
# e.g. (0,0) --> "a8"
#      "b4"  --> (1,4)
#      (3,6) --> "d2"
def board_to_coord(square):
    if square == (0, 0):
        return (-1, -1)
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
    def __init__(self, board, piece_set, piece, start_pos=None):
        pygame.sprite.Sprite.__init__(self)
        self.board = board
        self.piece_set = piece_set
        self.colour = piece[0]
        self.piece = piece[1]
        self.attached = False                   # Picked up with mouse
        self.status = True                      # Alive or Dead/True or False
        self.aggression = False
        self.moved = False

        self.image = pygame.image.load("src/pieces/{}/{}{}.png".format(self.piece_set, self.colour, self.piece))
        self.image = pygame.transform.scale(self.image, (self.board.screen.get_width()/8, self.board.screen.get_width()/8)).convert_alpha()
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
        if self.xy == (-1, -1):
            return
        if self.attached == True:
            self.aggression = True
            pos = pygame.mouse.get_pos()
            self.rect.x, self.rect.y = (pos[0] - self.rect.width/2, pos[1] - self.rect.width/2)
        elif self.attached == False:
            self.rect.x = (self.rect.x+50)//100*100
            self.rect.y = (self.rect.y+50)//100*100

            if self.check_position((self.rect.x//100, self.rect.y//100)):
                self.board.turn_end(self.colour, self.piece, self.xy, (self.rect.x//100, self.rect.y//100))    # only change turn if a piece changes position
                self.xy = (self.rect.x//100, self.rect.y//100)
                self.moved = True
            else:
                self.rect.x = self.xy[0]*100
                self.rect.y = self.xy[1]*100

            self.promote()  # Check for need to promote
            # Remove enemy piece if aggressive
            if self.aggression:
                # determine enemy
                if self.colour == "w":
                    enemy = self.board.black
                elif self.colour == "b":
                    enemy = self.board.white
                # Remove piece
                for piece in enemy:
                    if piece.xy == self.xy:
                        piece.remove()
                self.aggression = False
            
    def check_position(self, new_pos):
        def is_between(a,b,c):
            if a == c or b == c:
                return False
            # round to avoid extremely small differences in numbers
            return round(dist(a,c) + dist(b,c),2) == round(dist(a,b),2)

        if self.xy == new_pos:
            return False
        # check all of players own pieces, if moving into own piece, dont
        for piece in self.board.turn:
            if piece.xy == new_pos:
                return False
        # Check if a piece is inbetween start_pos and dest.
        # Because of a knights short path, a piece would need 
        #   a decimal x,y value to be inbetween its start and dest.
        # the knight abides by this because no piece can have a 
        #   coord with whole numbers in the (+1, +2) L shape the
        #   knight uses. Ie. (+0.5, +1.5)
        for piece in self.board.pieces:
            if is_between(self.xy, new_pos, piece.xy):
                return False

        match self.piece:
            case "p":
                if round(dist(self.xy, new_pos), 1) in (1.4,1.0,2.0):
                    if abs(self.xy[0] - new_pos[0]) == 1:
                        for piece in self.board.pieces:
                            if piece.xy == new_pos:
                                return True
                        return False
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
            case "r":
                if self.piece == "r":   # rook
                    if self.xy[0] == new_pos[0] or self.xy[1] == new_pos[1]:
                        return True
                    else:
                        return False
            case "b":
                if self.xy[0] == new_pos[0] or self.xy[1] == new_pos[1]:
                    return False
                if abs(slope(self.xy, new_pos)) == 1.0:
                    return True
                else:
                    return False
            case "n":
                if round(dist(self.xy, new_pos), 1) == 2.2:
                    return True
                else:
                    return False
            case "k":
                if round(dist(self.xy, new_pos), 1) == 1.4 or round(dist(self.xy, new_pos), 1) == 1.0:
                    return True
                elif round(dist(self.xy, new_pos), 1) == 2.0:
                    # castling
                    # if king has ever moved, then do not castle
                    if self.moved == True:
                        return False
                    # find appropiate rook, see if it has moved
                    for piece in self.board.turn:
                        # if it isnt a rook, skip
                        if not piece.piece == "r":
                            continue
                        # if it has moved, skip
                        if piece.moved == True:
                            continue
                        # if it is not in range, skip
                        if not round(dist(piece.xy, new_pos), 1) <= 2.0:
                            continue
                        if piece.xy[0] == 0:
                            piece.xy = (3, piece.xy[1])
                            piece.rect.x = piece.xy[0]*100
                        elif piece.xy[0] == 7:
                            piece.xy = (5, piece.xy[1])
                            piece.rect.x = piece.xy[0]*100
                        self.board.just_castled = True
                        return True
                else:
                    return False
            case "q":
                if self.xy[0] == new_pos[0] or self.xy[1] == new_pos[1]:
                    return True
                elif abs(slope(self.xy, new_pos)) == 1.0:
                    return True
                else:
                    return False
        return

    def promote(self):
        if self.piece == "p":
            if self.colour == "w" and self.rect.y//100 == 0 or self.colour == "b" and self.rect.y//100 == 7:
                self.piece = "q"
                self.image = pygame.image.load("src/pieces/{}/{}{}.png".format(self.piece_set, self.colour, self.piece))
                self.image = pygame.transform.scale(self.image, (self.board.screen.get_width()/8, self.board.screen.get_width()/8)).convert_alpha()
    def remove(self):
        if self.piece == "k":
            if self.colour == "w":
                self.board.winner = "Black"
            elif self.colour == "b":
                self.board.winner = "White"
            
        self.xy = (-1, -1)
        self.rect.x = self.xy[0]*100
        self.rect.y = self.xy[1]*100
    

class Board():
    def __init__(self, ctx):
        self.screen = ctx

        self.game_start = time()
        self.time = time()
        self.dt = 0
        self.moves = 0
        self.move_set = []

        self.chess_set = "cardinal_png"
        self.font = pygame.font.SysFont("FreeSans", 15, bold=True)

        self.white = []
        self.black = []
        self.pieces = self.white + self.black

        self.whitesprites = pygame.sprite.RenderPlain(self.white)
        self.blacksprites = pygame.sprite.RenderPlain(self.black)
        self.allsprites = pygame.sprite.RenderPlain(self.pieces)
        
        self.turn = self.white
        self.winner = None # Set to "Black" or "White" depending winner, set None if undecided
        
        self.just_castled = False


    def draw(self):
        box_width = self.screen.get_width() / 8
        box_colour = [(255,255,255), (0,0,0)]
        box_count = 0
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.screen, box_colour[box_count%2], (j*box_width,i*box_width,box_width,box_width))
                box_count += 1
            box_count += 1
        box_count = 1
        for engraving in range(8):
            # render numbers first
            engrave = self.font.render(str(8-engraving), False, box_colour[box_count%2])
            self.screen.blit(engrave, (5,100*engraving +5))
            box_count += 1
        box_count =0
        convert_table = ["A", "B", "C", "D", "E", "F", "G", "H"]
        for engraving in range(8):
            # render letters second
            engrave = self.font.render(str(convert_table[engraving]), False, box_colour[box_count%2])
            self.screen.blit(engrave, (100*engraving +85, 780))
            box_count += 1

    def default_game(self):
        self.game_start = time()
        self.time = time()
        self.dt = 0
        self.moves = 0
        self.move_set = []

        self.chess_set = "cardinal_png"
        #self.chess_set = "california_png"
        self.white = [
            ChessPiece(self, self.chess_set, "wp", "a2"),
            ChessPiece(self, self.chess_set, "wp", "b2"),
            ChessPiece(self, self.chess_set, "wp", "c2"),
            ChessPiece(self, self.chess_set, "wp", "d2"),
            ChessPiece(self, self.chess_set, "wp", "e2"),
            ChessPiece(self, self.chess_set, "wp", "f2"),
            ChessPiece(self, self.chess_set, "wp", "g2"),
            ChessPiece(self, self.chess_set, "wp", "h2"),
            ChessPiece(self, self.chess_set, "wr", "a1"),
            ChessPiece(self, self.chess_set, "wn", "b1"),
            ChessPiece(self, self.chess_set, "wb", "c1"),
            ChessPiece(self, self.chess_set, "wq", "d1"),
            ChessPiece(self, self.chess_set, "wk", "e1"),
            ChessPiece(self, self.chess_set, "wb", "f1"),
            ChessPiece(self, self.chess_set, "wn", "g1"),
            ChessPiece(self, self.chess_set, "wr", "h1")
        ]
        self.black = [
            ChessPiece(self, self.chess_set, "bp", "a7"),
            ChessPiece(self, self.chess_set, "bp", "b7"),
            ChessPiece(self, self.chess_set, "bp", "c7"),
            ChessPiece(self, self.chess_set, "bp", "d7"),
            ChessPiece(self, self.chess_set, "bp", "e7"),
            ChessPiece(self, self.chess_set, "bp", "f7"),
            ChessPiece(self, self.chess_set, "bp", "g7"),
            ChessPiece(self, self.chess_set, "bp", "h7"),
            ChessPiece(self, self.chess_set, "br", "a8"),
            ChessPiece(self, self.chess_set, "bn", "b8"),
            ChessPiece(self, self.chess_set, "bb", "c8"),
            ChessPiece(self, self.chess_set, "bq", "d8"),
            ChessPiece(self, self.chess_set, "bk", "e8"),
            ChessPiece(self, self.chess_set, "bb", "f8"),
            ChessPiece(self, self.chess_set, "bn", "g8"),
            ChessPiece(self, self.chess_set, "br", "h8")
        ]
        self.pieces = self.white + self.black
        
        self.whitesprites = pygame.sprite.RenderPlain(self.white)
        self.blacksprites = pygame.sprite.RenderPlain(self.black)
        self.allsprites = pygame.sprite.RenderPlain(self.pieces)
        
        self.turn = self.white
    
    def turn_end(self, color=None, piece=None, start_pos=None, end_pos=None):
        self.dt = time() - self.time
        self.time = time()
        # move_set entry: (turn_duration, color, piece, start_pos, end_pos)
        if color and piece and start_pos and end_pos:
            self.move_set.append((self.dt, color, piece, start_pos, end_pos))
        
        if self.just_castled:
            if piece == "k":
                if end_pos[0] == 2:
                    self.move_set.append((0.0, color, "r", (0, start_pos[1]), (3, end_pos[1])))
                if end_pos[0] == 6:
                    self.move_set.append((0.0, color, "r", (7, start_pos[1]), (5, end_pos[1])))

        self.moves += 1
        if self.turn is self.white:
            self.turn = self.black
        elif self.turn is self.black:
            self.turn = self.white

    def save_game(self):
        # (board, piece_set, piece, start_pos=None)
        board = []
        dead = []
        if self.turn is self.white:
            turn = "white"
        elif self.turn is self.black:
            turn = "black"

        for piece in self.pieces:
            if piece.xy == (-1, -1):
                # all dead pieces go to xy=(-1,-1)
                dead.append((piece.colour + piece.piece))
            else:
                board.append((piece.colour + piece.piece, piece.xy))
        
        data = [board, dead, turn, self.move_set]

        with open('game.chess', 'w') as filehandle:
            json.dump(data, filehandle, indent=2)
        
    def load_game(self):
        with open('game.chess', 'r') as filehandle:
            data = json.load(filehandle)

        self.white = []
        self.black = []

        colour = None
        # load alive pieces
        for piece in data[0]:
            if piece[0][0] == "w":
                colour = self.white
            if piece[0][0] == "b":
                colour = self.black
            colour.append(
                ChessPiece(self, self.chess_set, piece[0], coord_to_board(piece[1]))
            )
        # load dead pieces
        for piece in data[1]:
            if piece[0][0] == "w":
                colour = self.white
            if piece[0][0] == "b":
                colour = self.black
            colour.append(
                ChessPiece(self, self.chess_set, piece, (0, 0))
            )

        # reload data structures
        self.pieces = self.white + self.black
        
        self.whitesprites = pygame.sprite.RenderPlain(self.white)
        self.blacksprites = pygame.sprite.RenderPlain(self.black)
        self.allsprites = pygame.sprite.RenderPlain(self.pieces)
        
        # evalutate next turn
        if data[2] == "white":
            self.turn = self.white
        elif data[2] == "black":
            self.turn = self.black
        
        # load move history
        self.move_set = data[3]
    
    def get_valid_moves(self, piece_set):
        # (from, to)
        valid_moves = []
        for piece in piece_set:
            for x in range(8):
                for y in range(8):
                    if piece.check_position((x, y)):
                        valid_moves.append((piece.xy, (x, y)))
        return valid_moves
        
    def move_random_piece(self):
        moves = self.get_valid_moves(self.turn)
        move = moves[randint(0, len(moves)-1)]
        print(moves)
        print(move)
        for piece in self.turn:
            if piece.xy == (-1, -1):
                continue
            if move[0] == piece.xy:
                piece.rect.x = move[1][0]*100
                piece.rect.y = move[1][1]*100
                piece.aggression = True
                break


def main():
    pygame.init()

    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    board = Board(screen)
    board.default_game()

    while True:
        # Player Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("\n" + "="*28 + "\n\tGame Stats\n" + "="*28)
                print("Total Moves: {}\nPlay Time: {} seconds".format(board.moves, round(time() - board.game_start)))
                print()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                found_piece = find_closest(board.turn, mouse_pos)
                if not found_piece == None:
                    found_piece.attached = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                found_piece = find_closest(board.turn, mouse_pos)
                if not found_piece == None:
                    found_piece.attached = False
            
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    for piece in board.white + board.black:
                        if piece.piece == "p":
                            piece.remove()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    board.save_game()
                if event.key == pygame.K_a:
                    board.load_game()
                if event.key == pygame.K_r:
                    board.default_game()
                if event.key == pygame.K_c:
                    board.move_random_piece()


                    
        # Logical Updates
        #allsprites.update()
        board.whitesprites.update()
        board.blacksprites.update()
        
        #fps_counter = pygame.font.render("FPS:", ())
        fps_counter = board.font.render('FPS: {}'.format(str(round(clock.get_fps(), 1))), False, (150, 50, 50))
        
        if board.winner:
            winner_text = board.font.render("{} has won!".format(board.winner), False, (0,255,255))



        # Graphics Rendering
        board.draw()
        board.allsprites.draw(screen)

        screen.blit(fps_counter, (0,0))
        if board.winner:
            screen.blit(winner_text, (350,0))


        pygame.display.flip()

        clock.tick(60)
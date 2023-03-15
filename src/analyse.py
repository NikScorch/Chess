#!/usr/bin/python3
import pygame
import json
from chess import *

# check to make sure data doesnt change
def get_largest(dictionary, figures=1):
    data = list(dictionary.items())
    largest_values = []
    for i in range(figures):
        highest_value = ((0, 0), 0)
        for value in data:
            if highest_value[1] <= value[1]:
                highest_value = value
        largest_values.append(highest_value)
        data.remove(highest_value)
    return largest_values

def average_time(move_set):
    avg = 0
    div = len(move_set)
    for num in move_set:
        avg += num[0]
    avg = avg / div
    return avg

def stack_moves(base, stack):
    # layer multiple layers of data from different stacks onto the same base
    # populate with "move_to" data (not "move_from")
    for move in stack:
        base[tuple(move[4])] += 1
    return base
def stack_moves_file(base, file):
    with open(file, "r") as filehandler:
        data = json.load(filehandler)
    # layer multiple layers of data from different stacks onto the same base
    # populate with "move_to" data (not "move_from")
    for move in data[3]:
        base[tuple(move[4])] += 1
    return base

def heat_map(board_data, file):
    # "file" is save dir
    # assume chess board diction as input
    pygame.font.init()
    font = pygame.font.SysFont("FreeSans", 15, bold=True)
    map = pygame.Surface((800, 800))
    box_width = 100

    # get largest possible number, returns [(coord, val)], divid into 255 to get color increment value
    # this normalises the color in the heat maps, the most common value will always be RGB(255, 0, 0)
    increment = 255 / get_largest(board_data, 1)[0][1]

    # heat map
    for i in range(8):
        for j in range(8):
            # do not render a color greater than 255 (not possible), increase by increment values for each squares visit value
            pygame.draw.rect(map, (min(255, increment*board_data[(j, i)]), 0, 0), (j*box_width,i*box_width,box_width,box_width))
    # edge engravings
    for engraving in range(8):
            # render numbers first
            engrave = font.render(str(8-engraving), False, (255, 255, 255))
            map.blit(engrave, (5,100*engraving +5))
    convert_table = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for engraving in range(8):
        # render letters second
        engrave = font.render(str(convert_table[engraving]), False, (255, 255, 255))
        map.blit(engrave, (100*engraving +85, 780))
    pygame.image.save(map, file)
def heat_map_file(file, save):
    # "file" is open dir
    with open(file, "r") as filehandler:
        data = json.load(filehandler)
    
    squares = {}
    # populate with every chess square
    for x in range(0, 8):
        for y in range(0, 8):
            squares[(x, y)] = 0
    squares = stack_moves(squares, data[3])

    heat_map(squares, save)

def make_board():
    squares = {}
    # populate with every chess square
    for x in range(0, 8):
        for y in range(0, 8):
            squares[(x, y)] = 0
    return squares

def analyse(file):
    print("\n" + "="*28 + "\n\tGame Stats\n" + "="*28)
    print("Save File: {}\n".format(file))

    with open(file, "r") as filehandler:
        data = json.load(filehandler)
        
    print("Total moves:\t{}".format(len(data[3])))
    print("Pieces taken:\t{}".format(len(data[1])))
    print("Avg turn time:\t{} seconds".format(round(average_time(data[3]), 1)))


    squares = make_board()
    squares = stack_moves(squares, data[3])


    print("\nMost commonly vistied squares\n┏━━━━━━━┳━━━━━━━┓\n┃Square\t┃Count\t┃\n┣━━━━━━━╋━━━━━━━┫")
    most_visited_squares = get_largest(squares, 4)
    for i in most_visited_squares:
        print("┃ {}\t┃ {}\t┃".format(coord_to_board(i[0]), i[1]))
    print("┗━━━━━━━┻━━━━━━━┛")


def main():
    analyse("saves/game1.chess")
    analyse("saves/game2.chess")
    analyse("saves/game3.chess")
    analyse("saves/game4.chess")
    heat_map_file("saves/game1.chess", "stats/game1.png")
    heat_map_file("saves/game2.chess", "stats/game2.png")
    heat_map_file("saves/game3.chess", "stats/game3.png")
    heat_map_file("saves/game4.chess", "stats/game4.png")

    board = make_board()
    board = stack_moves_file(board, "saves/game1.chess")
    board = stack_moves_file(board, "saves/game2.chess")
    board = stack_moves_file(board, "saves/game3.chess")
    board = stack_moves_file(board, "saves/game4.chess")
    heat_map(board, "stats/avg.png")

    analyse("game.chess")
    heat_map_file("game.chess", "stats/game.png")

def main_pgn(dir):
    all_pgn = make_board()
    for i in range(1, 51):
        heat_map_file("{}/{}.chess".format(dir, i), "{}/{}.png".format(dir, i))
        all_pgn = stack_moves_file(all_pgn, "{}/{}.chess".format(dir, i))
    heat_map(all_pgn, "{}/avg.png".format(dir))
    
if __name__ == "__main__":
    main()
    main_pgn("pgn")

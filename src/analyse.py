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

def heat_map(file):
    with open(file, "r") as filehandler:
        data = json.load(filehandler)
    
    squares = {}
    # populate with every chess square
    for x in range(0, 8):
        for y in range(0, 8):
            squares[(x, y)] = 0
    squares = stack_moves(squares, data[3])

    screen = pygame.Surface((800, 800))
    box_width = 100
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, (20*squares[(j, i)], 0, 0), (j*box_width,i*box_width,box_width,box_width))
    pygame.image.save(screen, "stats/{}-heatmap.png".format(file.replace("/","_")))


def analyse(file):
    print("\n" + "="*28 + "\n\tGame Stats\n" + "="*28)
    print("Save File: {}\n".format(file))

    with open(file, "r") as filehandler:
        data = json.load(filehandler)
        
    print("Total moves:\t{}".format(len(data[3])))
    print("Pieces taken:\t{}".format(len(data[1])))
    print("Avg turn time:\t{} seconds".format(round(average_time(data[3]), 1)))


    squares = {}
    # populate with every chess square
    for x in range(0, 8):
        for y in range(0, 8):
            squares[(x, y)] = 0
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

    heat_map("saves/game1.chess")
    heat_map("saves/game2.chess")
    heat_map("saves/game3.chess")
    heat_map("saves/game4.chess")

if __name__ == "__main__":
    main()

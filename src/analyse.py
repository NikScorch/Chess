#!/usr/bin/python3
from chess import *

import json
with open("game.chess", "r") as filehandler:
    data = json.load(filehandler)
    
print("Total moves:\t{}".format(len(data[3])))
print("Pieces taken:\t{}".format(len(data[2])))


squares = {}
for x in range(0, 8):
    for y in range(0, 8):
        squares[(x, y)] = 0

# populate with move_to data (not move from)
for move in data[3]:
    squares[tuple(move[4])] += 1

most_common_square = coord_to_board(max(squares, key=squares.get))
most_common_square_uses = max(squares.values())
print("Most commonly moved to square: {}\nMoved to {} times"
      .format(most_common_square, most_common_square_uses))


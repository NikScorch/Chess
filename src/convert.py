#!/bin/python3
# util to convert .pgn files to .chess
from chess import board_to_coord
from json import dump

def format(dir, file):
    with open(dir + "/" + file) as fp:
        data = fp.read()

    # remove ending newline and split
    data = data[:-2]
    data = data.split("\n\n")

    # pair correct headers with move sets
    data_new = []
    for i, string in enumerate(data):
        if i % 2 == 1:
            continue
        data_new.append(data[i] + "\n\n" + data[i+1])

    # save to a file
    for i, string in enumerate(data_new):
        with open("{}/{}.pgn".format(dir, i+1), "w") as fp:
            fp.write(string)

def convert(infile, outfile, verbose=False):
    with open(infile) as file:
        pgn = file.read()

    pgn = pgn.split("\n")
    while pgn[0] == "" or pgn[0][0] == "[":
        pgn.pop(0)
    pgn = " ".join(pgn)
    pgn = pgn.split(" ")

    for i in pgn:
        if "." in i:
            pgn.remove(i)

    for i in range(len(pgn)):
        pgn[i] = pgn[i].replace("x", "")
        pgn[i] = pgn[i].replace("+", "")
        pgn[i] = pgn[i].replace("#", "")
        pgn[i] = pgn[i].replace("=Q", "")   
    pgn.pop()   # remove score from end

    pieces = "KQRBNP" 
    board = [
        [],     # board pieces
        [],     # dead pieces
        "",     # turn
        []      # move set
    ]
    for i, move in enumerate(pgn):
        chess_move = [0.0, "b", "kqrnbp", (0,0), (7,7)]
        if i % 2 == 0:
            chess_move[1] = "w"

        # TODO: cannot process castling, ignore for now, add dummy move
        if move[:3] == "O-O":
            if chess_move[1] == "w":
                row = 7
                if move == "O-O-O":
                    board[3].append([0.0, "w", "k", [4, row], [6, row]])
                    board[3].append([0.0, "w", "r", [7, row], [5, row]])
                if move == "O-O":
                    board[3].append([0.0, "w", "k", [4, row], [2, row]])
                    board[3].append([0.0, "w", "r", [0, row], [3, row]])
            if chess_move[1] == "b":
                row = 0
                if move == "O-O-O":
                    board[3].append([0.0, "b", "k", [4, row], [6, row]])
                    board[3].append([0.0, "b", "r", [7, row], [5, row]])
                if move == "O-O":
                    board[3].append([0.0, "b", "k", [4, row], [2, row]])
                    board[3].append([0.0, "b", "r", [0, row], [3, row]])
            continue
            # white O-O-O
            # [0.0, "w", "k", [4, 7], [2, 7]], 
            # [0.0, "w", "r", [0, 7], [3, 7]]

            # black O-O-O
            # [0.0, "b", "k", [4, 0], [2, 0]], 
            # [0.0, "b", "r", [0, 0], [3, 0]]


            # white O-O
            # [0.0, "w", "k", [4, 7], [6, 7]], 
            # [0.0, "w", "r", [0, 7], [5, 7]]

            # black O-O
            # [0.0, "b", "k", [4, 0], [6, 0]], 
            # [0.0, "b", "r", [0, 0], [5, 0]]

        # (time, who, what, where_from, where_to)
        if move[0] in pieces:
            chess_move[2] = move[0].lower()
        else:
            chess_move[2] = "p"
        try: 
            chess_move[4] = board_to_coord(move[-2:])
        except Exception:
            print(move)
            print(board)

        board[3].append(chess_move)

    with open(outfile, "w") as fp:
        dump(board, fp, indent=2)

    if verbose == True:
        for i, value in enumerate(pgn):
            print(value, end="\t")
            if i % 2 == 0:
                print("")
        print(board)

def main():
    format("pgn", "chess_com_games_2023-03-05.pgn")
    for i in range(1, 51):
        convert("pgn/{}.pgn".format(i), "pgn/{}.chess".format(i))

if __name__ == "__main__":
    main()
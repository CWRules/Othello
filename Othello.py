"""Othello

Othello-playing AI using breadth-first tree search.
"""

import tree_builder


def print_board(board):
    """Returns a string which represents a board state graphically."""
    ret_string = ' '
    for i in range(len(board[0])):
        ret_string += ' {}'.format(i)
    for row in range(len(board)):
        ret_string += '\n{}|'.format(row)
        for cell in board[row]:
            ret_string += cell + '|'
    return ret_string


def get_score(board):
    """Returns a tuple representing the score of each player on the given board."""
    black = 0
    white = 0
    for row in board:
        for cell in row:
            if cell == 'B':
                black += 1
            elif cell == 'W':
                white += 1
    return (black, white)


def read_board(filename):
    """Reads board state from file and returns it as a list of lists."""
    board = []
    with open(filename) as f:
        for line in f:
            line = line.strip('\r\n')
            line = line.replace('-', ' ')
            board.append(list(line))
    return board


# Initial setup
while True:
    player_color = raw_input('Select AI color (B/W): ').upper()
    if player_color == 'B' or player_color == 'W':
        break
    else:
        print 'Invalid selection'

MAX_TIME = 30
start_board = read_board('starting_board.txt')

root_node = tree_builder.Node(start_board)
if root_node.turn != player_color:
    tree_builder.make_tree(root_node, MAX_TIME)


# Main loop
while True:
    print '\nTurn {} - {}\n{}\n'.format(root_node.depth + 1, root_node.turn, print_board(root_node.board))

    if root_node.turn == player_color:
        # Build tree and select best move
        tree_builder.make_tree(root_node, MAX_TIME)

        print 'Best move is {0}, value {1:.3f}'.format(root_node.best_child_node.move, root_node.value)
        root_node = root_node.best_child_node
    else:
        if root_node.children[0].move == 'skip':
            print 'Opponent has no legal moves'
            root_node = root_node.children[0]
        else:
            # Enter opponent's move
            while True:
                move_coords = raw_input('Enter move (row column): ').split()
                if len(move_coords) == 2 and move_coords[0].isdigit() and move_coords[1].isdigit():
                    move = (int(move_coords[0]), int(move_coords[1]))
                else:
                    print 'Invalid selection'
                    continue
                new_node = None
                for child_node in root_node.children:
                    if child_node.move == move:
                        new_node = child_node
                if new_node != None:
                    root_node = new_node
                    break
                else:
                    print 'Selection is not a legal move'

    if root_node.game_over:
        break
    tree_builder.prune_tree(root_node)

# Game over
print '\nGame over'
(black, white) = get_score(root_node.board)
if black > white:
    print 'B wins!'
elif black < white:
    print 'W wins!'
else:
    print 'It\'s a tie!'
print '{} - {}'.format(black, white)

raw_input("Press Enter to exit\n")

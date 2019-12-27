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


# Initial setup
while True:
    player_color = raw_input('Select AI color (B/W): ').upper()
    if player_color == 'B' or player_color == 'W':
        break
    else:
        print 'Invalid selection'

MAX_DEPTH = 5
start_board = [[' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ','W','B',' ',' ',' '],
               [' ',' ',' ','B','W',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' ']]

root_node = tree_builder.Node(start_board)
if root_node.turn != player_color:
    tree_builder.make_tree(root_node, MAX_DEPTH)


# Main loop
while True:
    print '\nTurn {} - {}\n{}'.format(root_node.depth + 1, root_node.turn, print_board(root_node.board))

    if root_node.turn == player_color:
        # Build tree and select best move
        tree_builder.make_tree(root_node, root_node.depth + MAX_DEPTH)

        print 'Best move is {}, value {}'.format(root_node.best_child_node.move, root_node.value)
        root_node = root_node.best_child_node
    else:
        # Enter opponent's move
        while True:
            move_coords = raw_input('Enter opponent\'s move (row column): ').split()
            if move_coords[0] == 'skip':
                move = 'skip'
            elif len(move_coords) == 2 and move_coords[0].isdigit() and move_coords[1].isdigit():
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
score = tree_builder.evaluate_board(root_node.board, True)
if score > 0:
    print 'B wins!'
elif score < 0:
    print 'W wins!'
else:
    print 'It\'s a tie!'

raw_input("Press Enter to exit\n")

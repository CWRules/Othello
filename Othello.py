"""Othello"""

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


start_board = [[' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ','W','B',' ',' ',' '],
               [' ',' ',' ','B','W',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' ']]

print print_board(start_board)
root_node = tree_builder.Node(start_board)
tree_builder.make_tree(root_node, 6)

if root_node.best_child_node == False:
    print 'Game is over'
else:
    print 'Best move is {}, value {}'.format(root_node.best_child_node.move, root_node.value)
    print print_board(root_node.best_child_node.board)

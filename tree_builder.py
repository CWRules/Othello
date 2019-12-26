"""Tree Builder

Build tree of possible board states, then evaluate terminal nodes and propogate upwards with min-max.
"""

import copy, time

class Node:
    """Class to define single node in tree."""
    def __init__(self, board, parent_node = None, move = None):
        self.children = []
        self.value = 0
        self.best_child_node = None
        self.game_over = False
        self.move = move
        self.board = board

        # Check if this is the root node
        if parent_node.__class__.__name__ == 'Node':
            self.parent = parent_node
            parent_node.children.append(self)
            
            if parent_node.turn == 'B':
                self.turn = 'W'
            else:
                self.turn = 'B'
        else:
            # For root node, define initial game state
            self.turn = 'B'


def check_validity(board, row, col, color):
    """Function to check if a move is valid for a given board state.

    Returns False if the move is not legal, otherwise returns the board state after the move is made.
    """
    cells_to_flip = []
    
    for direction in ((-1,-1),( 0,-1),( 1,-1),( 1, 0),( 1, 1),( 0, 1),(-1, 1),(-1, 0)):
        current_row = row + direction[0]
        current_col = col + direction[1]
        new_cells = []
        while ( current_row >= 0 and current_row < len(board) and
                current_col >= 0 and current_col < len(board[current_row]) ):
            if board[current_row][current_col] == ' ':
                break
            elif board[current_row][current_col] == color:
                cells_to_flip += new_cells
                break
            else:
                new_cells.append((current_row, current_col))
                
            current_row += direction[0]
            current_col += direction[1]

    if len(cells_to_flip) > 0:
        new_board = copy.deepcopy(board)
        new_board[row][col] = color
        for cell in cells_to_flip:
            new_board[cell[0]][cell[1]] = color
        return new_board
    else:
        return False


def make_children(parent_node):
    """Function to build the tree of board states."""
    for row in range(len(parent_node.board)):
        for col in range(len(parent_node.board[row])):
            if parent_node.board[row][col] == ' ':
                new_board = check_validity(parent_node.board, row, col, parent_node.turn)
                if new_board != False:
                    Node(new_board, parent_node, (row, col))
                    
    if len(parent_node.children) == 0:
        Node(parent_node.board, parent_node, 'skip')


def evaluate_board(board, finished):
    """Returns the value of a board state.

    Positive values are good for black, negative is good for white.
    Currently just counts the number of stones of each color.
    """
    black = 0
    white = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'B':
                black += 1
            elif board[row][col] == 'W':
                white += 1
                
    if finished:
        if black > white:
            return 1000
        if black < white:
            return -1000
        else:
            return 0
    else:
        return black - white


def evaluate_node(current_node, depth):
    """Determines the value of a node in the tree.

    Called recursively to propogate the values upwards using min-max.
    Returns maximum recursion depth.
    """
    if len(current_node.children) == 0:
        current_node.value = evaluate_board(current_node.board, current_node.game_over)
    else:
        depth = evaluate_node(current_node.children[0], depth + 1)
        best_node = current_node.children[0]
        for child_node in current_node.children[1:]:
            evaluate_node(child_node, depth + 1)
            if ( (current_node.turn == 'B' and child_node.value > best_node.value) or
                 (current_node.turn == 'W' and child_node.value < best_node.value) ):
                best_node = child_node
        current_node.value = best_node.value
        current_node.best_child_node = best_node
    return depth


def make_tree(root_node, search_time):
    """Given a starting board state, builds and evaluates the search tree."""
    node_list = [root_node]
    start_time = time.time()
    print 'Starting tree search (cut off after {}s)'.format(search_time)

    while len(node_list) > 0 and time.time() - start_time < search_time:
        current_node = node_list.pop(0)

        # See if the game is over
        if current_node.move != 'skip' or current_node.parent.move != 'skip':
            make_children(current_node)
            node_list += current_node.children
        else:
            current_node.game_over = True
    print 'Finished tree search, starting evaluation'

    # Evaluate nodes
    start_time = time.time()
    max_depth = evaluate_node(root_node, 0)
    print 'Evaluation finished after {0:.3f}s'.format(time.time() - start_time)
    print 'Looked {} moves ahead'.format(max_depth)


# TODO: Move this into a new file and convert this into a module

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


# Testing
start_board = [[' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ','W','B',' ',' ',' '],
               [' ',' ',' ','B','W',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' '],
               [' ',' ',' ',' ',' ',' ',' ',' ']]

print print_board(start_board)
root_node = Node(start_board)
make_tree(root_node, 10)

if root_node.best_child_node == False:
    print 'Game is over'
else:
    print 'Best move is {}, value {}'.format(root_node.best_child_node.move, root_node.value)
    print print_board(root_node.best_child_node.board)

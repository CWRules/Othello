"""Tree Builder

Build tree of possible board states, then evaluate terminal nodes and propogate upwards with min-max.
"""

import copy, time, random
random.seed()


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
            
            self.depth = parent_node.depth + 1
        else:
            self.turn = 'B'
            self.depth = 0


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
        new_node = Node(parent_node.board, parent_node, 'skip')
        
        # See if the game is over
        if parent_node.move == 'skip':
            new_node.game_over = True


def evaluate_board(node):
    """Returns the value of the board state for a given node.

    Positive values are good for black, negative is good for white.
    
    Three heuristics are used:
    1) Number of discs of each color. If the game is over, this is the only heuristic used.
    2) A bonus for stable discs (ie. discs that cannot possibly be flipped)
    3) A random modifier. This makes the AI less predictable, and incentivizes moves that provide more options.
    """
    score = 0
    for row in node.board:
        for cell in row:
            if cell == 'B':
                score += 1
            elif cell == 'W':
                score -= 1
                
    if node.game_over:
        return score * 1000
    else:
        score += compute_stability(node.board)
        return score + random.random()


def compute_stability(board):
    """Computes the stability value of a given board state.

    For a disc to be stable, it must be stable in on all four axes (N-S, W-E, NW-SE, NE-SW).
    
    To be stable on one axis, one of the following must be true:
    1) The disc is on the edge of the board.
    2) The axis has no empty cells.
    3) There is an adjacent stable disc of the same color.
    
    1 and 2 are checked for every stone on the first pass.
    3 is checked repeatedly until no new stable discs are found.
    """
    stable_discs = set()
    for row in range(len(board)):
        max_row = len(board)
        for col in range(len(board[row])):
            max_col = len(board[row])
            if board[row][col] != ' ':
                stable_axes = { ((-1,-1),( 1, 1)): False,
                                (( 0,-1),( 0, 1)): False,
                                (( 1,-1),(-1, 1)): False,
                                (( 1, 0),(-1, 0)): False }

                # Edge of board?
                for axis in stable_axes:
                    if ( row + axis[0][0] < 0 or row + axis[0][0] >= max_row or
                         col + axis[0][1] < 0 or col + axis[0][1] >= max_col or
                         row + axis[1][0] < 0 or row + axis[1][0] >= max_row or
                         col + axis[1][1] < 0 or col + axis[1][1] >= max_col ):
                        stable_axes[axis] = True

                # No empty cells?
                for axis in stable_axes:
                    if stable_axes[axis] == False:
                        axis_full = True
                        for direction in axis:
                            current_row = row + direction[0]
                            current_col = col + direction[1]
                            while ( current_row >= 0 and current_row < max_row and
                                    current_col >= 0 and current_col < max_col ):
                                if board[current_row][current_col] == ' ':
                                    axis_full = False
                                    break
                                current_row += direction[0]
                                current_col += direction[1]
                        if axis_full:
                            stable_axes[axis] = True

                # If disc is stable, add it to the set
                stable_disc = True
                for axis in stable_axes:
                    if stable_axes[axis] == False:
                        stable_disc = False
                if stable_disc:
                    stable_discs.add((row, col))


    # TODO: Propogate stability to adjacent discs and compute stability heuristic value
    return 0


def evaluate_node(current_node):
    """Determines the value of a node in the tree.

    Called recursively to propogate the values upwards using min-max.
    """
    if len(current_node.children) == 0:
        current_node.value = evaluate_board(current_node)
    else:
        depth = evaluate_node(current_node.children[0])
        best_node = current_node.children[0]
        for child_node in current_node.children[1:]:
            evaluate_node(child_node)
            if ( (current_node.turn == 'B' and child_node.value > best_node.value) or
                 (current_node.turn == 'W' and child_node.value < best_node.value) ):
                best_node = child_node
        current_node.value = best_node.value
        current_node.best_child_node = best_node


def make_tree(root_node, search_time):
    """Given a starting board state, builds and evaluates the search tree.

    Each time a new tree level is reached, estimate how long it will take to generate.
    If the estimate plus the current time is longer than max search time, end the search.
    """
    node_list = [root_node]
    last_depth = root_node.depth

    print 'Starting tree search (target time {}s)'.format(search_time)
    start_time = time.time()
    level_start_time = time.time()
    level_nodes_visited = 0
    
    while len(node_list) > 0:
        current_node = node_list.pop(0)
        if current_node.depth != last_depth:
            # See if we need to cut off the tree search
            if ((time.time() - level_start_time) / level_nodes_visited) * len(node_list) > search_time:
                print 'Ending search at depth {}'.format(last_depth - root_node.depth)
                break
            else:
                last_depth = current_node.depth
                level_start_time = time.time()
                level_nodes_visited = 0
        level_nodes_visited += 1
        if len(current_node.children) == 0 and current_node.game_over == False:
            make_children(current_node)
        node_list += current_node.children
    print 'Finished tree search after {0:.3f}s'.format(time.time() - start_time)

    print 'Starting evaluation'
    start_time = time.time()
    evaluate_node(root_node)
    print 'Evaluation finished after {0:.3f}s'.format(time.time() - start_time)


def prune_tree(root_node):
    """Deletes parent of root_node and all other children.

    The garbage collector deals with the orphaned nodes if we just break one link.
    """
    root_node.parent.children.remove(root_node)
    root_node.parent = None
        

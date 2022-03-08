        #!/usr/bin/python
#
### Student Info
# Smith, Christopher, 02386569, 159.302
# Assignment 1: 8 Puzzle.
#
### Language
# This assignment was written in Python. An open source, interpreted language
# with a mix of imperative, OO and functional programming. Syntax is simple
# and easy to learn.
#
# Developed on Ubuntu Linux but this will run on the interpreter available
# from http://python.org. Documentation is also on that site but a good
# tutorial is available for free at http://diveintopython.org.
#
### Data Structures
#
# The state of the board is stored in a list. The list stores values for the
# board in the following positions:
#
# -------------
# | 0 | 3 | 6 |
# -------------
# | 1 | 4 | 7 |
# -------------
# | 2 | 5 | 8 |
# -------------
#
# The goal is defined as:
#
# -------------
# | 1 | 2 | 3 |
# -------------
# | 8 | 0 | 4 |
# -------------
# | 7 | 6 | 5 |
# -------------
#
# Where 0 denotes the blank tile or space.
goal_state = [1, 8, 7, 2, 0, 6, 3, 4, 5]
#
# The code will read state from a file called "state.txt" where the format is
# as above but space seperated. i.e. the content for the goal state would be
# 1 8 7 2 0 6 3 4 5

### Code begins.
import sys
from pythonds.basic.stack import Stack
from operator import attrgetter


def display_board(state):
    print( "-------------")
    print( "| %i | %i | %i |" % (state[0], state[3], state[6]))
    print( "-------------")
    print( "| %i | %i | %i |" % (state[1], state[4], state[7]))
    print( "-------------")
    print( "| %i | %i | %i |" % (state[2], state[5], state[8]))
    print( "-------------")


def move_up(state):
    """Moves the blank tile up on the board. Returns a new state as a list."""
    # Perform an object copy
    new_state = state[:]
    index = new_state.index(0)
    # Sanity check
    if index not in [0, 3, 6]:
        # Swap the values.
        temp = new_state[index - 1]
        new_state[index - 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move, return None (Pythons NULL)
        return None


def move_down(state):
    """Moves the blank tile down on the board. Returns a new state as a list."""
    # Perform object copy
    new_state = state[:]
    index = new_state.index(0)
    # Sanity check
    if index not in [2, 5, 8]:
        # Swap the values.
        temp = new_state[index + 1]
        new_state[index + 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move, return None.
        return None


def move_left(state):
    """Moves the blank tile left on the board. Returns a new state as a list."""
    new_state = state[:]
    index = new_state.index(0)
    # Sanity check
    if index not in [0, 1, 2]:
        # Swap the values.
        temp = new_state[index - 3]
        new_state[index - 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move it, return None
        return None


def move_right(state):
    """Moves the blank tile right on the board. Returns a new state as a list."""
    # Performs an object copy. Python passes by reference.
    new_state = state[:]
    index = new_state.index(0)
    # Sanity check
    if index not in [6, 7, 8]:
        # Swap the values.
        temp = new_state[index + 3]
        new_state[index + 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move, return None
        return None


def create_node(state, parent, operator, depth, cost):
    return Node(state, parent, operator, depth, cost)


def expand_node(node):
    """Returns a list of expanded nodes"""
    expanded_nodes = []
    expanded_nodes.append(create_node(move_up(node.state), node, "u", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_down(node.state), node, "d", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_left(node.state), node, "l", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_right(node.state), node, "r", node.depth + 1, 0))
    # Filter the list and remove the nodes that are impossible (move function returned None)
    expanded_nodes = [node for node in expanded_nodes if node.state != None]  # list comprehension!
    return expanded_nodes


def bfs(start, goal):
    """Performs a breadth first search from the start state to the goal"""
    # A list (can act as a queue) for the nodes.
    goal=goal
    start_node=create_node(start,None,None,0,0)
    fringe=[]
    fringe.append(start_node)
    current=fringe.pop(0)
    path=[]
    while(current.state!=goal):
        fringe.extend(expand_node(current))
        current=fringe.pop(0)
    while(current.parent!=None):
        path.insert(0,current.operator)
        current=current.parent
    return path
    pass


def dfs(start, goal, depth=10):
    start_node=create_node(start,None,None,0,0)
    fringe_stack=Stack()
    fringe_stack.push(start_node)
    current=fringe_stack.pop()
    path=[]
    while(current.state!=goal):
        temp=expand_node(current)
        for item in temp:
            fringe_stack.push(item)
        current=fringe_stack.pop()
        if(current.depth>10):
            return None
    while(current.parent!=None):
        path.insert(0,current.operator)
        current=current.parent
    return path


#uniform cost
def ucs(start,goal):
    start_node=create_node(start,None,None,0,0)
    fringe=[]
    path=[]
    fringe.append(start_node)
    current=fringe.pop(0)
    while(current.state!=goal):
        temp=expand_node(current)
        for item in temp:
            item.depth+=current.depth
            fringe.append(item)
        fringe.sort(key =lambda x: x.depth)
        current=fringe.pop(0)
    while(current.parent!=None):
        path.insert(0,current.operator)
        current=current.parent
    return path


def greedy(start,goal):
    start_node=create_node(start,None,None,0,0)
    fringe=[]
    path=[]
    fringe.append(start_node)
    current=fringe.pop(0)
    while(current.state!=goal):
        fringe.extend(expand_node(current))
        for item in fringe:
            h(item,goal)
        fringe.sort(key =lambda x: x.heuristic)
        current=fringe.pop(0)
    while(current.parent!=None):
        path.insert(0,current.operator)
        current=current.parent
    return path


def a_star(start, goal):
    start_node=create_node(start,None,None,0,0)
    fringe=[]
    path=[]
    fringe.append(start_node)
    current=fringe.pop(0)
    while(current.state!=goal):
        fringe.extend(expand_node(current))
        for item in fringe:
            h(item,goal)
            item.heuristic+=item.depth
        fringe.sort(key =lambda x: x.heuristic)
        current=fringe.pop(0)
    while(current.parent!=None):
        path.insert(0,current.operator)
        current=current.parent
    return path


def h(state, goal):
    dmatch=0
    for i in range(0,9):
        if state.state[i] != goal[i]:
            dmatch+=1
    state.heuristic=dmatch


# Node data structure
class Node:
    def __init__(self, state, parent, operator, depth, cost):
        # Contains the state of the node
        self.state = state
        # Contains the node that generated this node
        self.parent = parent
        # Contains the operation that generated this node from the parent
        self.operator = operator
        # Contains the depth of this node (parent.depth +1)
        self.depth = depth
        # Contains the path cost of this node from depth 0. Not used for depth/breadth first.
        self.cost = cost

        self.heuristic=None


def readfile(filename):
    f = open(filename)
    data = f.read()
    # Get rid of the newlines
    data = data.strip('|')
    # Break the string into a list using a space as a seperator.
    data = data.split(" ")
    state = []
    for element in data:
        state.append(int(element))
    print('state: ', state)
    return state


# Main method
def main():
    starting_state = readfile(r"state.txt")
    ### CHANGE THIS FUNCTION TO USE bfs, dfs, ids or a_star
    # result = a_star(starting_state, goal_state)
    # result = bfs(starting_state, goal_state)
    # result = dfs(starting_state, goal_state)
    result = ucs(starting_state, goal_state)
    if result == None:
        print( "No solution found")
    elif result == [None]:
        print( "Start node was the goal!")
    else:
        print(result)
        print(len(result), " moves")


# A python-isim. Basically if the file is being run execute the main() function.
if __name__ == "__main__":
    main()
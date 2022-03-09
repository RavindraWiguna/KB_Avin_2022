from collections import Counter
from turtle import distance #to act like a std::map on cpp

#reference: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2 08/03/2022
class PuzzleNode():
    """A node class for 8 Puzzle"""
    def __init__(self, parent=None, position=None, prev_move=None):
        self.parent = parent #a string of 9 char
        self.position = position #also a string of 9 char
        self.prev_move = prev_move
        self.g = 0 #cost from start node
        self.h = 0 #estimated cost to end node
        self.f = 0 #total cost

    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        return self.position

#GLOBAL VARIABLE
GOAL_NODE = None #will be created after readfile
GOAL_POS = None #hold row, col data for each number in goal
MOVE_SET = [
    ['l', 'u'],             #0
    ['r', 'l', 'u'],        #1
    ['r', 'u'],             #2
    ['l', 'd', 'u'],        #3
    ['r', 'l', 'd', 'u'],   #4
    ['r', 'd', 'u'],        #5
    ['l', 'd'],             #6
    ['r', 'l', 'd'],        #7
    ['r', 'd']              #8
]

def readfile(filename):
    f = open(filename)
    data = f.read()
    # print(data) #is a string
    return data

def get_pos_from_str(string_state):
    positions = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]
    for id, c in enumerate(string_state):
        c = int(c)
        row, col = id//3, id%3
        positions[c].append(row)
        positions[c].append(col)
    
    return positions


def get_heuristic_val(game_position):
    global GOAL_POS
    total_distance = 0
    for id, c in enumerate(game_position):
        c = int(c)
        if(c == 0):#skip 0 position
            continue
        row, col = id//3, id%3
        distance = abs(GOAL_POS[c][0] - row) + abs(GOAL_POS[c][1] - col)
        total_distance += distance
    return total_distance

def a_star(game_state, zero_id):
    pass

def greedy_best_first(game_state):
    pass

def check_data(datas):
    for data in datas:
        print(data)

def main():
    global GOAL_NODE, GOAL_POS
    #read the goal and initial state
    init_state = readfile("state.txt")
    goal_state = readfile("goal.txt")
    
    #create nodes based on those state
    start_node = PuzzleNode(None, init_state)
    GOAL_NODE = PuzzleNode(None, goal_state)
    
    #extract each number row/col position for heuristic
    GOAL_POS = get_pos_from_str(GOAL_NODE.position)

    h = get_heuristic_val(start_node.position)
    print(h)









if __name__ == "__main__":
    main()
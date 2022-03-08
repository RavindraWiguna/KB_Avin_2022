from collections import Counter #to act like a std::map on cpp

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

def get_string_state(game_state):
    game_string = ""
    for row in game_state:
        for i in row:
            game_string+=str(i)
    # print(game_string)
    return game_string

def get_heuristic_val(game_position):
    global GOAL_NODE
    goal_position = GOAL_NODE.position
    #loop through position


def a_star(game_state, zero_id):
    pass

def greedy_best_first(game_state):
    pass

def check_data(datas):
    for data in datas:
        print(data)

def main():
    global GOAL_NODE
    init_state = readfile("state.txt")
    goal_state = readfile("goal.txt")

    start_node = PuzzleNode(None, init_state)
    GOAL_NODE = PuzzleNode(None, goal_state)

    get_heuristic_val(start_node.position)
    









if __name__ == "__main__":
    main()
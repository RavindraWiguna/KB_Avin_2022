from collections import Counter #to act like a std::map<str, int> on cpp
from queue import PriorityQueue #to store node with automated queue based on f val
import os #for debuging (pause on windows)
from copy import deepcopy
import time

from numpy import Inf 

#pseudocode reference: 
#Wikipedia: Pseudocode on A star with some googling of python data structures, but modified f(n) instead of g(n)+h(n) become only h(n)
GROUND = ord("0") #to help convert str to int
class PuzzleNode():
    """A node class for 8 Puzzle"""
    def __init__(self, state=None, paths=None):
        self.state = state #a string of 9 char
        self.paths = paths #[r, l, d, u] move to get from parrent to this node
        self.h = 0
        self.zero_id = None #location of "0" in the string to fasten look up for moveset

        #search for 0
        # print(type(self.state))
        for id, c in enumerate(self.state):
            c = ord(c) - GROUND
            if(c == 0):
                self.zero_id = id
                # print(f'zero id: {id}')
                break
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __gt__(self, other):
        return self.h > other.h

    def __str__(self):
        return self.state
    


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
INFINITY = float('inf')


def readfile(filename):
    f = open(filename)
    data = f.read()
    # print(data) #is a string
    return data

def get_pos_from_state(string_state):
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
        c = ord(c) - GROUND
        row, col = id//3, id%3
        positions[c].append(row)
        positions[c].append(col)
    
    return positions

def get_heuristic_val(node_state):
    global GOAL_POS
    total_distance = 0
    for id, c in enumerate(node_state):
        c = int(c)
        if(c == 0):#skip 0 position
            continue
        row, col = id//3, id%3
        distance = abs(GOAL_POS[c][0] - row) + abs(GOAL_POS[c][1] - col)
        total_distance += distance
    return total_distance

def create_state(cur_node, move):
    state_list = list(cur_node.state) #because string is immutable
    num_id = 0 #swapped number index
    if(move == 'r'):
        #zero to left
        num_id = cur_node.zero_id - 1
    elif (move == 'l'):
        #zero to right
        num_id = cur_node.zero_id + 1
    elif (move == 'u'):
        #zero to down
        num_id = cur_node.zero_id + 3
    else:
        #zero to up
        num_id = cur_node.zero_id - 3
    
    #swap
    state_list[cur_node.zero_id] = state_list[num_id] #set 0 to number
    state_list[num_id] = "0" #set the num to 0

    state_str = "".join(state_list)
    # print(state_list)
    #return the state
    return state_str

total_node = 0
def greedy_bestfs(start_node):
    global GOAL_NODE, MOVE_SET, total_node
    
    open_nodes = PriorityQueue()#store node that haven't explored with pqueue
    closed_state = Counter() #counter for state that has been explored
    
    #node scores
    start_node.h = get_heuristic_val(start_node.state)
    open_nodes.put(start_node)
    
    path = None #saved path for return value
    total_node+=1
    isNotFound = True
    #loop while open list is not empty in pythonic way
    while open_nodes and isNotFound:
        #get node with min f value
        min_node = open_nodes.get()
        
        #get all possible move
        possible_move = MOVE_SET[min_node.zero_id]
        for move in possible_move:
            #generate node based on move
            move_state = create_state(min_node, move)
            # print(move_state)
            cur_min_path = deepcopy(min_node.paths)
            cur_min_path.append(move)
            move_node = PuzzleNode(move_state, cur_min_path)
            # os.system("pause")
            #check if this node's state has been reached/visited/closed
            if(closed_state[move_node.state] > 0):
                continue
            
            if(move_node == GOAL_NODE):
                print("HEY, Found the goal!")
                path = move_node.paths
                isNotFound = False
                break

            #this node has not visited add to queue, but first calc the h
            #add min node counter in 
            closed_state[move_node.state]+=1
            move_node.h = get_heuristic_val(move_node.state)
            open_nodes.put(move_node)
            total_node+=1
            

        #End of For Loop
    #End of While Loop
    return path

def check_data(datas):
    for data in datas:
        print(data)

def main():
    global GOAL_NODE, GOAL_POS, total_node
    #read the goal and initial state
    init_state = readfile("state.txt")
    goal_state = readfile("goal.txt")
    
    print(init_state)
    print(goal_state)
    #create nodes based on those state
    start_node = PuzzleNode(init_state, ["."])
    GOAL_NODE = PuzzleNode(goal_state, ["."])
    
    #extract each number row/col position for heuristic calculation
    GOAL_POS = get_pos_from_state(GOAL_NODE.state)

    #search!
    start_time = time.perf_counter()
    path = greedy_bestfs(start_node)
    end_time = time.perf_counter()
    print(f'Greedy Best First Search elapsed times: {end_time - start_time}')
    print(f'Total node opened: {total_node}')
    print(path)
    print(f'total move: {len(path)}')



if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()')
    main()
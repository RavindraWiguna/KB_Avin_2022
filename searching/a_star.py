from collections import Counter #to act like a std::map<str, int> on cpp
from collections import defaultdict #dictionary but with default value on missing key
from queue import PriorityQueue #to store node with automated queue based on f val
import os #for debuging (pause on windows)
import time 

#pseudocode reference: 
#https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#https://en.wikipedia.org/wiki/A*_search_algorithm
#GLOBAL VARIABLE
GOAL_NODE = None #will be created after readfile
GOAL_POS = None #hold row, col data for each number in goal
CHANGE_MOVE_ID = {'r': -1, 'l':1, 'u':3, 'd':-3}
GROUND = ord("0") #to help convert str to int

class PuzzleNode():
    """A node class for 8 Puzzle"""
    def __init__(self, state=None, prev_move=None, zero_id=None):
        self.state = state #a string of 9 char
        self.prev_move = prev_move #[r, l, d, u] move to get from parrent to this node
        self.f = 0
        self.zero_id = zero_id #location of "0" in the string to fasten look up for moveset
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __gt__(self, other):
        return self.f > other.f

def readfile(filename):
    f = open(filename)
    data = f.read()
    # print(data) #is a string
    zero_id = 0
    for id, element in enumerate(data):
        if(element=="0"):
            zero_id = id
            break
    
    return data, zero_id

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
    global CHANGE_MOVE_ID
    state_list = list(cur_node.state) #because string is immutable
    num_id = cur_node.zero_id + CHANGE_MOVE_ID[move] #swapped number index
    #swap
    state_list[cur_node.zero_id] = state_list[num_id] #set 0 to number
    state_list[num_id] = "0" #set the num to 0

    state_str = "".join(state_list)
    # print(state_list)
    #return the state
    return state_str, num_id

def reconstruct_path(node, cameFrom):
    path = []
    cur_node = node
    while(cur_node.prev_move != "."):
        path.append(cur_node.prev_move)
        cur_node = cameFrom[cur_node.state]
    
    path.append(".")#append "."
    return path[::-1] #return the reversed the path

def print_state(state, goal):
    print("====INITIAL STATE==================GOAL STATE=====")
    print( "+-----+-----+-----+            +-----+-----+-----+")
    print("|     |     |     |            |     |     |     |")
    print(f'|  {state[0]}  |  {state[1]}  |  {state[2]}  |            |  {goal[0]}  |  {goal[1]}  |  {goal[2]}  |')
    print("|     |     |     |            |     |     |     |")
    print("+-----+-----+-----+            +-----+-----+-----+")
    print("|     |     |     |            |     |     |     |")
    print(f'|  {state[3]}  |  {state[4]}  |  {state[5]}  |  INTO ==>  |  {goal[3]}  |  {goal[4]}  |  {goal[5]}  |')
    print("|     |     |     |            |     |     |     |")
    print("+-----+-----+-----+            +-----+-----+-----+")    
    print("|     |     |     |            |     |     |     |")
    print(f'|  {state[6]}  |  {state[7]}  |  {state[8]}  |            |  {goal[6]}  |  {goal[7]}  |  {goal[8]}  |')
    print("|     |     |     |            |     |     |     |")
    print("+-----+-----+-----+            +-----+-----+-----+") 

def a_star(start_node):
    global GOAL_NODE
    MOVE_SET = (
    ('l', 'u'),             #0
    ('r', 'l', 'u'),        #1
    ('r', 'u'),             #2
    ('l', 'd', 'u'),        #3
    ('r', 'l', 'd', 'u'),   #4
    ('r', 'd', 'u'),        #5
    ('l', 'd'),             #6
    ('r', 'l', 'd'),        #7
    ('r', 'd')              #8
    )
    total_opened_node = 0
    open_nodes = PriorityQueue()#store node that haven't explored with pqueue
    closed_state = Counter() #counter for state that has been explored
    cameFrom = {} #dict to map where a node came from
    
    #node scores
    gScore = defaultdict(lambda:float('inf'))
    gScore[start_node.state] = 0 #save start node state gscore to 0
    start_node.f = get_heuristic_val(start_node.state) 
    open_nodes.put(start_node)
    total_opened_node+=1
    path = None #saved path for return value
    tentative_gScore = None #variable to hold min node gScore
    #loop while open list is not empty in pythonic way
    while open_nodes:
        #get node with min f value
        min_node = open_nodes.get()
        #add min node counter in 
        closed_state[min_node.state]+=1
        
        #check if it is the goal node
        if (min_node == GOAL_NODE):
            print("HEY, Found the goal!")
            path = reconstruct_path(min_node, cameFrom)
            break
        
        #get all possible move
        possible_move = MOVE_SET[min_node.zero_id]
        # print(f'got {len(possible_move)} possible move')
        for move in possible_move:
            #generate node based on move
            move_state, move_zero = create_state(min_node, move)
            # print(move_state)
            move_node = PuzzleNode(move_state, move, move_zero)
            # os.system("pause")
            #check if this node's state has been reached/visited/closed
            if(closed_state[move_node.state] > 0):
                continue
            
            # print(f'{move_node.state}')
            #calculate f value of this node
            tentative_gScore = gScore[min_node.state] + 1 #distance of node is same, so always +1
            if(tentative_gScore < gScore[move_node.state]):
                cameFrom[move_node.state] = min_node
                gScore[move_node.state] = tentative_gScore
                move_node.f = tentative_gScore + get_heuristic_val(move_node.state)
                #check if it is not in the open set
                if(move_node not in (x for x in open_nodes.queue)):
                    total_opened_node+=1
                    open_nodes.put(move_node)

        #End of For Loop
    #End of While Loop
    return path, total_opened_node

def main():
    global GOAL_NODE, GOAL_POS
    #read the goal and initial state
    init_state, init_zero = readfile("state.txt")
    goal_state, goal_zero = readfile("goal.txt")
    
    print_state(init_state, goal_state)
    #create nodes based on those state
    start_node = PuzzleNode(init_state, ".", init_zero)
    GOAL_NODE = PuzzleNode(goal_state, ".", goal_zero)
    
    #extract each number row/col position for heuristic calculation
    GOAL_POS = get_pos_from_state(GOAL_NODE.state)

    #search!
    print("Searching the Solution using A* Algorithm...")
    start_time = time.perf_counter()
    path, total_opened_node = a_star(start_node)
    end_time = time.perf_counter()
    print(f'A star elapsed times: {end_time - start_time}')
    print(f'Total node opened: {total_opened_node}')
    print(f'Total move: {len(path)}')
    print(f'Path:\n{path}')


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()')
    main()
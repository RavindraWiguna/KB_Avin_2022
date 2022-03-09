from collections import Counter #to act like a std::map on cpp
import os #for debuging (pause on windows)
import time 

#pseudocode reference: 
#https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2 08/03/2022
class PuzzleNode():
    """A node class for 8 Puzzle"""
    def __init__(self, parent=None, state=None, prev_move=None):
        self.parent = parent #a node :D
        self.state = state #also a string of 9 char
        self.prev_move = prev_move #[r, l, d, u] move to get from parrent to this node
        self.g = 0 #cost from start node
        self.h = 0 #estimated cost to end node
        self.f = 0 #total cost
        self.zero_id = None #location of "0" in the string to fasten look up for moveset
        #search for 0
        # print(type(self.state))
        for id, c in enumerate(self.state):
            c = int(c)
            if(c == 0):
                self.zero_id = id
                # print(f'zero id: {id}')
                break



    def __eq__(self, other):
        return self.state == other.state

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
        c = int(c)
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

def get_min_node(open_list):
    min_node = open_list[0] #set current min node as the first element
    node_id = 0 #id to be removed from open list
    for id, node in enumerate(open_list):
        if(node.f < min_node.f):
            #update the node and id
            min_node = node
            node_id = id
    
    return min_node, node_id

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
        num_id = cur_node.zero_id + 2
    else:
        #zero to up
        num_id = cur_node.zero_id - 2
    
    #swap
    state_list[cur_node.zero_id] = state_list[num_id] #set 0 to number
    state_list[num_id] = "0" #set the num to 0

    state_str = "".join(state_list)
    # print(state_list)
    #return the state
    return state_str

def reconstruct_path(node):
    path = []
    cur_node = node
    while(cur_node is not None):
        path.append(cur_node.prev_move)
        cur_node = cur_node.parent
    
    return path[::-1] #return the reversed the path

total_node = 0
def a_star(start_node):
    global GOAL_NODE, MOVE_SET, total_node
    open_nodes = [] #store node that haven't explored
    closed_state = Counter() #store state that has been explored
    path = None #saved path for return value
    open_nodes.append(start_node) #put start node on the open list
    total_node+=1
    #loop while open list is not empty in pythonic way
    while open_nodes:
        #get node with min f value
        min_node, node_id = get_min_node(open_nodes)
        #remove the min node from open list
        open_nodes.pop(node_id)
        #add min node counter in 
        closed_state[min_node.state]+=1
        
        #check if it is the goal node
        if (min_node == GOAL_NODE):
            print("HEY, Found the goal!")
            path = reconstruct_path(min_node)
            break
        
        #get all possible move
        possible_move = MOVE_SET[min_node.zero_id]
        # print(f'got {len(possible_move)} possible move')
        for move in possible_move:
            #generate node based on move
            move_state = create_state(min_node, move)
            # print(move_state)
            move_node = PuzzleNode(min_node, move_state, move)
            # os.system("pause")
            #check if this node's state has been reached/visited/closed
            if(closed_state[move_node.state] > 0):
                continue
            
            # print(f'{move_node.state}')
            #calculate f value of this node
            move_node.g = min_node.g + 1
            move_node.h = get_heuristic_val(move_node.state)
            move_node.f = move_node.g + move_node.h

            worthyToAdd = True
            #check this node duplicate on open_nodes using linear search
            for node in open_nodes:
                if(move_node == node):
                    if(move_node.g > node.g):
                        #same node exist but with lower g cost, so threw this node
                        worthyToAdd = False
                        break
            
            if(worthyToAdd):
                total_node +=1
                open_nodes.append(move_node)
        #End of For Loop
    #End of While Loop
    return path

def greedy_best_first(game_state):
    pass

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
    start_node = PuzzleNode(None, init_state)
    GOAL_NODE = PuzzleNode(None, goal_state)
    
    #extract each number row/col position for heuristic calculation
    GOAL_POS = get_pos_from_state(GOAL_NODE.state)

    #search!
    start_time = time.perf_counter()
    path = a_star(start_node)
    end_time = time.perf_counter()
    print(f'A star elapsed times: {end_time - start_time}')
    print(f'Total closed node inspected: {total_node}')
    print(path)
    print(f'total move: {len(path)}')



if __name__ == "__main__":
    main()

#some improvement:
'''
1. node aint counting zero everytime?
2. aint using string?, use array is ok, because 9 integer vs 9 char is kinda the same, but when counting of course using str hmm, so maybe still str
3. cek validity of 0 movement
4. shi idk, use more counter?
'''
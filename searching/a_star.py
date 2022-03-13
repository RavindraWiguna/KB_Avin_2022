from collections import Counter #to act like a std::map<str, int> on cpp
from collections import defaultdict #dictionary but with default value on missing key
from queue import PriorityQueue #to store node with automated queue based on f val
import time
from common_func import *

#pseudocode reference: 
#https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#https://en.wikipedia.org/wiki/A*_search_algorithm
def a_star(start_node, goal_node):
    total_opened_node = 0
    #extract each number row/col position for heuristic calculation
    goal_pos = get_pos_from_state(goal_node.state)
    
    open_nodes = PriorityQueue()#store node that haven't explored with pqueue
    closed_state = Counter() #counter for state that has been explored
    cameFrom = {} #dict to map where a node came from
    
    #node scores
    gScore = defaultdict(lambda:float('inf'))
    gScore[start_node.state] = 0 #save start node state gscore to 0
    start_node.h = get_heuristic_val(start_node.state, goal_pos) 
    start_node.f = start_node.h
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
        if (min_node == goal_node):
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
            move_node = AStarNode(move_state, move, move_zero)
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
                move_node.h = get_heuristic_val(move_node.state, goal_pos)
                move_node.f = tentative_gScore + move_node.h
                #check if it is not in the open set
                if(move_node not in open_nodes.queue):
                    total_opened_node+=1
                    open_nodes.put(move_node)

        #End of For Loop
    #End of While Loop
    return path, total_opened_node

def main():
    #read the goal and initial state
    init_state, init_zero = readfile("state.txt")
    goal_state, goal_zero = readfile("goal.txt")
    
    print_state(init_state, goal_state)
    #create nodes based on those state
    start_node = AStarNode(init_state, ".", init_zero)
    goal_node = AStarNode(goal_state, ".", goal_zero)
    
    #search!
    print("Searching Solution using A* Algorithm...")
    start_time = time.perf_counter()
    path, total_opened_node = a_star(start_node, goal_node)
    end_time = time.perf_counter()
    print(f'A star elapsed times: {end_time - start_time}')
    print(f'Total node opened: {total_opened_node}')
    print(f'Total move: {len(path)-1} (Without root)')
    print(f'Path:\n{path}')


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()')
    main()
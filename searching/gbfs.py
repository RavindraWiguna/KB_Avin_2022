from collections import Counter #to act like a std::map<str, int> on cpp
from queue import PriorityQueue #to store node with automated queue based on f val
import time

from common_func import *

#pseudocode reference: 
#modifitying A star with pseudocode from: https://en.wikipedia.org/wiki/Best-first_search

def greedy_best_first_search(start_node, goal_node):
    total_opened_node = 0
    goal_pos = get_pos_from_state(goal_node.state) #extract each number row/col position for heuristic calculation
    
    queue = PriorityQueue()#store node that haven't explored with pqueue
    visited = Counter() #counter for state that has been explored
    cameFrom = {}
    
    #node scores
    start_node.h = get_heuristic_val(start_node.state, goal_pos) 
    queue.put(start_node)
    total_opened_node+=1
    path = None #saved path for return value
    isFound = False
    #loop while open list is not empty in pythonic way
    while queue and not isFound:
        #get node with min f value
        min_node = queue.get()
        
        if(min_node == goal_node):
            print("HEY, Found the goal!")
            path = reconstruct_path(min_node, cameFrom)
            isFound = True
            break

        #get all possible move
        possible_move = MOVE_SET[min_node.zero_id]
        for move in possible_move:
            #generate node based on move
            move_state, move_zero = create_state(min_node, move)
            move_node = GreedyNode(move_state, move, move_zero)
            
            #check if this node's state has been reached/visited/closed
            if(visited[move_node.state] > 0):
                continue
            
            #this node has not visited so, add to queue, but first calc the h val
            move_node.h = get_heuristic_val(move_node.state, goal_pos)
            queue.put(move_node)
            cameFrom[move_node.state] = min_node
            #mark this node as visited 
            visited[move_node.state]+=1
            total_opened_node+=1     

        #End of For Loop
    #End of While Loop
    return path, total_opened_node

def main():
    #read the goal and initial state
    init_state, init_zero = readfile("state.txt")
    goal_state, goal_zero = readfile("goal.txt")
    
    print_state(init_state, goal_state)
    #create nodes based on those state
    start_node = GreedyNode(init_state, ".", init_zero)
    goal_node = GreedyNode(goal_state, ".", goal_zero)

    #search!
    print("Searching Solution using Greedy Best First Search Algorithm...")
    start_time = time.perf_counter()
    path, total_opened_node = greedy_best_first_search(start_node, goal_node)
    end_time = time.perf_counter()
    print(f'Greedy Best First Search elapsed times: {end_time - start_time}')
    print(f'Total node opened: {total_opened_node}')
    print(f'Total move: {len(path)-1} (Without root)')
    print(f'Path:\n{path}')


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()')
    main()
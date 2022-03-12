from common_func import readfile, print_state, create_state, MOVE_SET, BaseNode
from collections import Counter
import random as rd

def shuffle_node(node: BaseNode, n: int):
    visited = Counter()
    while(n > 0):
        possible_move = MOVE_SET[node.zero_id]
        possible_move = list(possible_move)
        isVisited = False
        while(not isVisited and possible_move):
            pick_move = rd.choice(possible_move)
            possible_move.remove(pick_move)

            state, zero_loc = create_state(node, pick_move)
            node = BaseNode(state, ".", zero_loc)
            if(visited[node.state] == 0):
                isVisited = True
                visited[node.state]+=1
        
        #aight, so we made new node that havent visited, then loop again
        n-=1
    
    return node



def main():
    goal_state, zero_id = readfile("goal.txt")
    # print_state(goal_state, goal_state)
    finish_node = shuffle_node(BaseNode(goal_state, ".", zero_id), 69420)
    print_state(goal_state, finish_node.state)
    print(finish_node.state)


if __name__=="__main__":
    main()


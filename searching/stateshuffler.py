from common_func import readfile, print_state, create_state, MOVE_SET, AStarNode
from collections import Counter
import random as rd

def shuffle_node(node, n: int):
    visited = Counter()
    while(n > 0):
        possible_move = MOVE_SET[node.zero_id]
        possible_move = list(possible_move)
        isVisited = False
        while(not isVisited and possible_move):
            pick_move = rd.choice(possible_move)
            possible_move.remove(pick_move)

            state, zero_loc = create_state(node, pick_move)
            node = AStarNode(state, ".", zero_loc)
            if(visited[node.state] == 0):
                isVisited = True
                visited[node.state]+=1
        
        #aight, so we made new node that havent visited, then loop again
        n-=1
    
    return node

def dfs_shuffle(init_node, n:int):
    Stacc = []
    visited = Counter()
    Stacc.append((init_node, 0))
    deep = 0
    furthest_node = None
    deepest = -1
    while Stacc and deep < n:
        cur_node, deep = Stacc.pop()
        if(deepest < deep):
            furthest_node = cur_node
            deepest = deep
        if(visited[cur_node.state] == 0):
            visited[cur_node.state]+=1
            possible_move = MOVE_SET[cur_node.zero_id]
            for move in possible_move:
                move_state, zero_loc = create_state(cur_node, move)
                move_node = AStarNode(move_state, move, zero_loc)
                Stacc.append((move_node, deep+1))
    
    if(Stacc):
        print(f'got furthest in stacc: {Stacc[-1][1]}')
        return Stacc[-1][0]
    print(f'got furthest ever: {deepest}')
    return furthest_node

def main():
    goal_state, zero_id = readfile("goal.txt")
    # print_state(goal_state, goal_state)
    # finish_node = shuffle_node(BaseNode(goal_state, ".", zero_id), 69420)
    finish_node = dfs_shuffle(AStarNode(goal_state, ".", zero_id), 2**18)
    print_state(goal_state, finish_node.state)
    print(finish_node.state)


if __name__=="__main__":
    main()


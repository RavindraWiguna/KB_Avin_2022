from copy import deepcopy
import time
import os
from collections import Counter

from cv2 import threshold
GOAL_STATE=[[],[],[]]
GROUND = ord("0")
def getStringState(game_state):
    game_string = ""
    for row in game_state:
        for i in row:
            game_string+=str(i)
            # game_string += chr(GROUND+i)
    # print(game_string)
    return game_string

def getChildState(zero_id):
    childs = [
        ['l', 'u'], #0
        ['r', 'l', 'u'], #1
        ['r', 'u'], #2
        ['l', 'd', 'u'], #3
        ['r', 'l', 'd', 'u'], #4
        ['r', 'd', 'u'], #5
        ['l', 'd'], #6
        ['r', 'l', 'd'], #7
        ['r', 'd'] #8
    ]
    return childs[zero_id]

def move_state(game_state, movement, zero_id):
    row_zero = zero_id//3
    col_zero = zero_id % 3
    # print(f'r: {row_zero}| c: {col_zero}')
    zero_temp = zero_id
    if(movement == "u"):
        #zero down
        game_state[row_zero][col_zero] = game_state[row_zero+1][col_zero]
        game_state[row_zero+1][col_zero] = 0
        zero_temp = (row_zero+1)*3 + col_zero
    elif (movement == "d"):
        game_state[row_zero][col_zero] = game_state[row_zero-1][col_zero]
        game_state[row_zero-1][col_zero] = 0
        zero_temp = (row_zero-1)*3 + col_zero
    elif (movement == "l"):
        game_state[row_zero][col_zero] = game_state[row_zero][col_zero+1]
        game_state[row_zero][col_zero+1] = 0
        zero_temp = (row_zero)*3 + col_zero+1
    else:
        game_state[row_zero][col_zero] = game_state[row_zero][col_zero-1]
        game_state[row_zero][col_zero-1] = 0
        zero_temp = (row_zero)*3 + col_zero-1                     
    return game_state, zero_temp
        
def state_is_a_goal(game_state):
    result = True
    for row in range(3):
        if(result):
            for col in range(3):
                if(game_state[row][col] != GOAL_STATE[row][col]):
                    result = False
                    break
        else:
            break
    return result


dfs_m_visited = {}
path_dfs = []
threshold = 10
def dfs(game_state, zero_id, depth):
    if(depth > threshold):
        return
    # Label this state as visited
    game_string = getStringState(game_state)
    dfs_m_visited[game_string] = 1
    # print(dfs_m_visited["123804765"]) error, use try
    possible_move = getChildState(zero_id)
    temp_state = deepcopy(game_state)
    for move in possible_move:
        path_dfs.append(move)
        temp_state, temp_zero = move_state(temp_state, move, zero_id)
        #check if it is not visited
        cur_temp_string = getStringState(temp_state)
        try:
            if(dfs_m_visited[cur_temp_string] == 1):
                #already visited
                pass
            else:
                print("should not be here")
        except KeyError:
            #never seen
            dfs_m_visited[cur_temp_string] = 1
            #check if it is goal
            # print(cur_temp_string)
            if(state_is_a_goal(game_state)):
                #yeayy
                print("got it")
                break
            else:
                #call dfs
                dfs(temp_state, temp_zero, depth+1)

        temp_state = deepcopy(game_state)
        #remove the saved path then
        # print("not this path")
        # os.system("pause")
        path_dfs.pop()
    
    # print("result is:")
    # print(path_dfs)


bfs_m_visited = Counter()
total_visited = 0
def bfs(game_state, zero_id):
    global bfs_m_visited, total_visited
    queue = []
    cur_state_str = getStringState(game_state)
    bfs_m_visited[cur_state_str]+= 1
    total_visited+=1
    last_path = ["Root"]
    the_path = []
    saved_state = deepcopy(game_state)
    saved_path = deepcopy(last_path)
    queue.append([saved_state, zero_id, saved_path])
    while(queue):
        # print(f'{len(queue)} left')
        #get queue1
        cur_que_state = deepcopy(queue[0][0])
        cur_que_zero = deepcopy(queue[0][1])
        cur_que_path = deepcopy(queue[0][2])
        # print(cur_que_path)
        # print(type(cur_que_path))
        #pop it
        queue.pop(0)
        # print(f'after: {len(queue)}')
        # print(cur_que_state)
        # os.system("pause")
        
        #cek if it is a goal
        if(state_is_a_goal(cur_que_state)):
            print("got it!")
            the_path = deepcopy(cur_que_path)
            break
        else:
            #go to each child
            possible_move = getChildState(cur_que_zero)
            preserved_state = deepcopy(cur_que_state)
            preserved_zero = deepcopy(cur_que_zero)
            preserved_path = deepcopy(cur_que_path)
            # print(f'it has: {len(possible_move)} possible move')
            # visited = 0
            for move in possible_move:
                #gerakin
                # print(move)
                # os.system("pause")
                this_move_path = deepcopy(cur_que_path)
                this_move_path.append(move)
                # print(this_move_path)
                # print(f'the move: {type(this_move_path)}')
                cur_que_state, cur_que_zero = move_state(cur_que_state, move, cur_que_zero)
                #cek is visited?
                cur_que_str = getStringState(cur_que_state)
                if(bfs_m_visited[cur_que_str] == 0):
                    # print(f'{cur_que_str} got added to queue')
                    bfs_m_visited[cur_que_str] += 1
                    total_visited+=1
                    #add to queue
                    # print(f'add: {type(this_move_path)}')
                    queue.append([cur_que_state, cur_que_zero, this_move_path])
                
                #reset
                cur_que_state = deepcopy(preserved_state)
                cur_que_zero = deepcopy(preserved_zero)
                cur_que_path = deepcopy(preserved_path)
        
        # print("done")

    return the_path

def readfile(filename):
    f = open(filename)
    data = f.read()
    # Break the string into a list using a space as a seperator.
    # data = data.split("")
    state = [[], [], []]
    cur_row = 0
    cur_data = 0
    cur_id = 0
    zero_id = 0
    for element in data:
        element = ord(element) - GROUND
        if(element == 0):
            zero_id = cur_id
        state[cur_row].append(element)
        cur_data+=1
        cur_id+=1
        if(cur_data == 3):
            cur_data = 0
            cur_row+=1

    print('state: ', state)
    return state, zero_id

def main():
    global GOAL_STATE
    game_state, zero_id = readfile("state.txt")
    GOAL_STATE, _temp = readfile("goal.txt")
    # print(zero_id)
    # dfs(game_state, zero_id, 0)
    # result = path_dfs
    start_time = time.perf_counter()
    result = bfs(game_state, zero_id)
    end_time = time.perf_counter()
    print(f'BFS elapsed times: {end_time - start_time}')
    print(f'total node visited = {total_visited}')
    print("we got:")
    if(len(result) > 0):
        print(result)
    else:
        print("nothing")

    print(f'total move: {len(result)}')
    # print(state_is_a_goal(GOAL_STATE))

if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()')
    main()
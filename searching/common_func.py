GROUND = ord("0") #to help convert str to int
CHANGE_MOVE_ID = {'r': -1, 'l':1, 'u':3, 'd':-3}
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

class BaseNode():
    """A base node class for 8 puzzle greedy and a star"""
    def __init__(self, state=None, prev_move=None, zero_id=None):
        self.state = state #a string of 9 char
        self.zero_id = zero_id #location of zero in the state
        self.prev_move = prev_move #previous move to get to this node
    
    def __eq__(self, other) -> bool:
        return self.state == other.state


class GreedyNode(BaseNode):
    """Node class for Greedy 8 Puzzle"""
    def __init__(self, state=None, prev_move=None, zero_id=None):
        super().__init__(state, prev_move, zero_id)
        self.h = 0
    
    def __gt__(self, other):
        return self.h > other.h

class AStarNode(BaseNode):
    """Node class for A star 8 puzzle"""
    def __init__(self, state=None, prev_move=None, zero_id=None):
        super().__init__(state, prev_move, zero_id)
        self.f = 0
    
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

def get_heuristic_val(node_state, GOAL_POS):
    total_distance = 0
    for id, c in enumerate(node_state):
        c = int(c)
        if(c == 0):#skip 0 position
            continue
        row, col = id//3, id%3
        distance = abs(GOAL_POS[c][0] - row) + abs(GOAL_POS[c][1] - col)
        total_distance += distance
    return total_distance

def create_state(cur_node: BaseNode, move: str):
    state_list = list(cur_node.state) #because string is immutable
    num_id = cur_node.zero_id + CHANGE_MOVE_ID[move] #swapped number index
    #swap
    state_list[cur_node.zero_id] = state_list[num_id] #set 0 to number
    state_list[num_id] = "0" #set the num to 0

    state_str = "".join(state_list)
    # print(state_list)
    #return the state
    return state_str, num_id

def print_state(state, goal):
    print("===[INITIAL STATE]================[GOAL STATE]====")
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

def reconstruct_path(min_node: BaseNode, cameFrom: dict):
    path = []
    cur_node = min_node
    while (cur_node.prev_move != "."):
        path.append(cur_node.prev_move)
        cur_node = cameFrom[cur_node.state]
    path.append("Root") #finally add the root
    return path[::-1] #reverse the path, and return it
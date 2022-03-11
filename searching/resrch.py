GROUND = ord("0") #to help convert str to int
class PuzzleNode():
    """A node class for 8 Puzzle"""
    def __init__(self, state=None, prev_move=None):
        self.state = state #also a string of 9 char
        self.prev_move = prev_move #[r, l, d, u] move to get from parrent to this node
        self.g = 0 #cost from start node
        self.h = 0 #estimated cost to end node
        self.f = 0 #total cost
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

    def __str__(self):
        return self.state


def main():
    #new object dict
    node_dict = {}
    node1 = PuzzleNode("102345678", ".")
    node2 = PuzzleNode("012345678", "r")
    node3 = PuzzleNode("312045678", "d")
    node_dict[node1.state] = node2
    node_dict[node2.state] = node3

    print(node_dict[node_dict[node1.state].state].state)


if __name__ == "__main__":
    main()
import time
import random
TENFIVE = 10**4

def ordf():
    ground = ord("0")
    char = "2"
    i = 0
    res = 0
    while( i < TENFIVE):
        res = ord(char) - ground
        i+=1

def intf():
    char = "2"
    i = 0
    res = 0
    while( i < TENFIVE):
        res = int(char)
        i+=1

def intcompsame():
    integers = 12345678
    new_int = 12345678
    i = 0
    while( i < TENFIVE):
        check = integers == new_int
        i+=1

def intcompdif():
    integers = 201345678
    new_int = 501234678
    i = 0
    while(i < TENFIVE):
        check = integers == new_int
        i+=1

def strcompsame():
    strings = "12345678"
    new_str = "12345678"
    i = 0
    while(i < TENFIVE):
        check = strings == new_str
        i+=1

def strcompdif():
    strings = "201345678"
    new_str = "501234678"
    i = 0
    while(i < TENFIVE):
        check = strings == new_str
        i+=1

def plusid():
    temp_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    tseven = 0
    i = 0
    while(i < TENFIVE):
        i+=1
        for id, el in enumerate(temp_arr):
            if(el == 7):
                tseven += id
                break
    
def overwriteid():
    temp_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    tseven = 0
    i = 0
    while(i < TENFIVE):
        i+=1
        for id, el in enumerate(temp_arr):
            if(el == 7):
                tseven = id
                break    

def dicteq():
    i = 0
    move=None
    change_move_id = {'r': -1, 'l': 1, 'u':3, 'd':-3}
    id = 5
    while(i < TENFIVE):
        i+=1
        move = random.choice(('l', 'r', 'd', 'u'))
        id += change_move_id[move]   

def ifelseeq():
    i = 0
    move = None
    id = 5
    while(i < TENFIVE):
        i+=1
        move = random.choice(('l', 'r', 'd', 'u'))
        if(move == 'r'):
            #zero to left
            id = id - 1
        elif (move == 'l'):
            #zero to right
            id = id + 1
        elif (move == 'u'):
            #zero to down
            id = id + 3
        else:
            #zero to up
            id = id - 3     

#=================================================
start_time = time.perf_counter()
ordf()
end_time = time.perf_counter()
print(f'elapsed time: {end_time - start_time}')


start_time = time.perf_counter()
intf()
end_time = time.perf_counter()
print(f'elapsed time: {end_time - start_time}')

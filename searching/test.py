import time

def ordf():
    ground = ord("0")
    char = "2"
    i = 0
    res = 0
    while( i < 100000):
        res = ord(char) - ground
        i+=1


def intf():
    char = "2"
    i = 0
    res = 0
    while( i < 100000):
        res = int(char)
        i+=1

def intcompsame():
    integers = 12345678
    new_int = 12345678
    i = 0
    while( i < 100000):
        check = integers == new_int
        i+=1



def intcompdif():
    integers = 201345678
    new_int = 501234678
    i = 0
    while(i < 100000):
        check = integers == new_int
        i+=1

def strcompsame():
    strings = "12345678"
    new_str = "12345678"
    i = 0
    while(i < 100000):
        check = strings == new_str
        i+=1

def strcompdif():
    strings = "201345678"
    new_str = "501234678"
    i = 0
    while(i < 100000):
        check = strings == new_str
        i+=1

start_time = time.perf_counter()

end_time = time.perf_counter()

print(f'elapsed time: {end_time - start_time}')

start_time = time.perf_counter()
strcompdif()
end_time = time.perf_counter()

print(f'elapsed time: {end_time - start_time}')
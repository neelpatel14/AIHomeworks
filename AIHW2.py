import random

# 0 represents the empty slot
goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]

def initialize_random_state():
    lst = []
    while len(lst) < 9:
        num = random.randint(0,8)
        if num not in lst:
            lst.append(num)
    return lst

def is_solved(my_lst):
    return my_lst == goal_state

def square_print(my_lst):
    if 0 in my_lst:
        index = my_lst.index(0)
        my_lst[index] = '-'
    for i in range(3):
        s = ""
        for j in range(3):
            s += str(my_lst[i*3+j]) + ' ' 
        print(s)

if __name__ == "__main__":
    lst = initialize_random_state()
    square_print(lst)

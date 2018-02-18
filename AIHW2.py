import random
import Queue
from copy import deepcopy

# 0 represents the empty slot
goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
found = set()

"""
Initializes a random state for the 8 puzzle.
"""
def initialize_random_state():
    lst = []
    while len(lst) < 9:
        num = random.randint(0,8)
        if num not in lst:
            lst.append(num)
    return lst

"""
Determines if a state is in the goal_state
"""
def is_solved(my_lst):
    return my_lst == goal_state

"""
Prints a state in the form of a 8 puzzle
"""
def square_print(my_lst):
    for i in range(3):
        s = ""
        for j in range(3):
            s += (str(my_lst[i*3+j]) if my_lst[i*3+j] else unichr(0x2588)) + ' ' 
        print(s)

"""
Hashes a state
"""
def list_to_num(my_lst):
    val = 0
    for i in my_lst:
        val = val*10 + i
    return val

"""
Determines if a state is solvable and provides the transitions if solvable
"""
def solve(my_lst):
    q = Queue.Queue()
    finished = True
    if not is_solved(my_lst):
        q.put((my_lst, [my_lst]))
        found.add(list_to_num(my_lst))
        neighs = [0, 1, 0, -1, 0]
        finished = False
    num_steps = 0
    while not q.empty() and not finished:
        tup = q.get() 
        state = tup[0]
        path = tup[1]
        loc = state.index(0) 
        loc_i = loc / 3
        loc_j = loc % 3
        for n_i in range(4):
            new_i = loc_i + neighs[n_i]
            new_j = loc_j + neighs[n_i + 1]
            if new_i < 0 or new_i > 2 or new_j < 0 or new_j > 2:
                continue
            new_loc = 3 * new_i + new_j
            copied = state[:]
            a = copied[new_loc]
            copied[new_loc] = 0
            copied[loc] = a
            state_num = list_to_num(copied)
            if state_num in found:
                continue
            if is_solved(copied):
                num_steps = len(path)
                for state_step in path:
                    square_print(state_step)
                    print("")
                finished = True
                break
            copied_path = path[:]
            copied_path.append(copied)
            q.put((copied, copied_path))
            found.add(state_num)
    if finished:
        square_print(goal_state)
        print("solved in %d steps" % num_steps)
    else:
        square_print(my_lst)
        print("unsolvable")

"""
Parses input to state
"""
def input_to_state(inp):
    state_strings = inp.split(" ")
    state = []
    for string in state_strings:
        state.append(int(string))
    return state

if __name__ == "__main__":
    print("Input a state represented as numbers 0 to 8")
    print("with spaces in between them. For example,")
    print("")
    print("0 1 2 3 4 5 6 7 8")
    print("")
    print("to represent")
    print("")
    s = unichr(0x2588) + " 1 2"
    print(s)
    print("3 4 5")
    print("6 7 8")
    print("")
    print("Enter 1 for randomized input. Enter 0 to quit")
    while True:
        print("")
        state = []
        state_string = raw_input("Enter a state: ")
        if state_string == "1":
            state = initialize_random_state()
        elif state_string == "0":
            print("Program terminated")
            break
        else:
            state = input_to_state(state_string)
        solve(state)

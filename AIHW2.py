import random

my_list = [] #initialize empty list



while len(my_list) < 9:
    num = random.randint(1, 9)
    if num not in my_list:
        my_list.append(num)


goal_state = sorted(my_list)
if(my_list == goal_state):
    print("You did it!")
else:
    print("u suk")

def square_print(my_list):
    if 9 in my_list:
        index = my_list.index(9)
        my_list[index] = '-'
    print(my_list[0:3])
    print(my_list[3:6])
    print(my_list[6:9])



square_print(my_list)

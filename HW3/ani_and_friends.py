import random
import json
import os.path
import time
import copy

TEAM_NAME = "ani and friends"
MEMBERS = ["np2ch", "ar9fh", "aml5ha"]  # Include a list of your members UVA IDs

# this is a test state function for you to drive the following test case with
# NOTE: you will receive this when the game playing program calls your get_move
# state = {
#     "game": "chicken",
#     "opponent-name": "the_baddies",
#     "team-code": "abc123",
#     "prev-response-time": 0.5,
#     "last-opponent-play": 0.71,
#     "last-outcome": -10,
# }
#
# state = {
#     "team-code": "eef8976e",
#     "game": "connect_more",
#     "opponent-name": "mighty_ducks",
#     "columns": 6,
#     "connect_n": 5,
#     "your-token": "R",
#     "board": [
#         ["R", "Y"],
#         ["R"],
#         [],
#         ["R", "Y", "Y", "Y"],
#         ["Y", "Y"],
#         [],
#     ]
# }
ani_and_friends_info_json = {"chicken": {}}

# This will load whatever dictionary you last saved, stub included to drive example,
#   isn't actual function
def load_info():
    return ani_and_friends_info_json["chicken"]
    """
    info = {}
    if os.path.isfile(info_filename):
        with open(info_filename, 'r') as info_file:
            info = json.load(info_file)
    return info
    """

# This will save (and overwrite) whatever dictionary you last saved
# Stub included to drive example, isn't actual function
def save_info(info):
    ani_and_friends_info_json["chicken"] = info
    """
    if True:#if state["game"] == "chicken":
        new_info = load_info()
        new_info.update(info)
        with open(info_filename, 'w') as info_file:
            json.dump(new_info, info_file)
    """

    """
    if state["game"] =="connect_more":
        #add new connect_more data to old data
    """

def get_stats(arr):
    mean = 0
    for i in arr:
        mean += i
    mean /= (1.0 * len(arr))
    std = 0
    for i in arr:
        std += (i - mean)**2
    std /= (len(arr) - 1)
    std = std ** (0.5)
    return mean, std

# returns a random move (for sake of example)
def get_chicken_move(state):
    info = load_info() # info might be "{}" if first use, otherwise reads dictionary from your save file
    if 'prev-response-time' in state and state["prev-response-time"] is not None:
        info.setdefault("response-times", []).append(state["prev-response-time"])
    # example for storing previous response times
    if 'last-opponent-play' in state and state["last-opponent-play"] is not None:
        if "opponents" not in info or state['opponent-name'] not in info['opponents']:
            info['opponent-sigmas'] = []
            if 'last-mean' in info:
                del info['last-mean']
        info.setdefault("opponents",{}).setdefault(state["opponent-name"],[]).append(state["last-opponent-play"])
    move = 10
    if "response-times" in info.keys() and len(info["response-times"]) > 9:
        sig = 1.29
        mean, std = get_stats(info["response-times"])
        if "last-mean" in info:
            info['opponent-sigmas'].append((state['last-opponent-play']-info['last-mean'])/info['last-std'])
            if len(info['opponent-sigmas']) > 3:
                sig_mean, sig_std = get_stats(info['opponent-sigmas'])
                if sig_std < 0.1 and sig_mean >= 1.24:
                    sig = sig_mean - 0.01
        info['last-mean'] = mean
        info['last-std'] = std
        move = min(mean + sig * std,10)
    info.setdefault("moves", []).append(move)
    if state["last-outcome"] is not None:
        info.setdefault("outcomes", []).append(state["last-outcome"])
    save_info(info)
    return {
        "move": move,
        "team-code": state["team-code"],
    }

def my_best_move(state):
        # timer for testing
        start_time = int(round(time.time() * 1000))
        # determine opponent's token
        if state["your-token"] == 'R':
            opp_token = 'Y'
        else:
            opp_token = 'R'

        # enumerate all legal moves
        # will map legal move states to their alpha values
        valid_moves = {}
        # check if the move is legal for each rowumn
        if state["columns"] < 7:
            for row in range(0, state["columns"]):
                # simulate the move in rowumn `row` for the current player
                tmp_state = simulate_move(state, row, state["your-token"])
                valid_moves[row] = -find(4, tmp_state, opp_token)                                           #SETTING DEPTH LEVEL
        else:
            for row in range(0, state["columns"]):
                # simulate the move in rowumn `row` for the current player
                tmp_state = simulate_move(state, row, state["your-token"])
                valid_moves[row] = -find(3, tmp_state, opp_token)                                           #SETTING DEPTH LEVEL

        best_alpha = -99999999
        best_move = None
        moves = valid_moves.items()
        ###print(moves)
        # search the best "move" with the highest `alpha` value
        #print(moves)
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        end_time = int(round(time.time() * 1000))
        print ("response time: ", (end_time - start_time))

        return best_move


def find(depth, state, curr_player_token):
    ###print("trying to find")
    ###print ("-------------STATE------------")
    ###print(state["board"])
    ###print("--------------END STATE--------")
    # enumerate all legal moves from this state
    legal_moves = []
    for i in range(0,state["columns"]):
        # simulate the move in rowumn i for curr_player
        tmp_state = simulate_move(dict(state), i, curr_player_token)
        legal_moves.append(tmp_state)

    if depth == 0 or len(legal_moves) == 0 or gameIsOver(state, curr_player_token):
        # return the heuristic value of node
        ###print(eval_game(state, curr_player_token))
        return eval_game(state, curr_player_token)

    # determine opponent's token
    if curr_player_token == "R":
        opp_player_token = "Y"
    else:
        opp_player_token = "R"

    alpha = -99999999
    for child in legal_moves:
        if child == None:
            continue
        alpha = max(alpha, -find(depth - 1, child, opp_player_token))
    # #print(alpha)
    return alpha


def simulate_move(state, rowumn, token):
    """
    Simulate a "move" in the grid `grid` by the current player with its token `token.
    :param grid: a grid of connect four
    :param rowumn: rowumn index
    :param token: token of a player
    :return tmp_grid: the new grid with the "move" just added
    """
    #redraw the board here
    ###print ("-------------STATE------------")
    ###print(state["board"])
    ###print("--------------END STATE--------")
    temp = copy.deepcopy(state)
    temp["board"][rowumn].append(token)
    # ##print("-------TEMP--------")
    # ##print(temp["board"])
    # ##print("-------END TEMP--------")
    return temp


def eval_game(state, curr_player_token):
        #This is where you can use my code (have to change how the counter works to count the streaks)
        # ##print("----------------BOARD----------------")
        # ##print(state["board"])
        if curr_player_token == "R":
            opp_token = "Y"
        else:
            opp_token = "R"
        # get scores of human and my player with theirs streaks
        n = state["connect_n"]
        my_list = []
        for i in range(2, n+1):
        	my_list.append(find_streak(state, curr_player_token, i))
       	opp_list = []

       	for j in range(2, n+1):
       		opp_list.append(find_streak(state, opp_token, j))

       	running_sum = 0
        opp_sum = 0
       	my_list.reverse()
       	opp_list.reverse()

        #print("----------------")
        #print(my_list)
        #print(opp_list)
        if opp_list[0] > 0:
            ##print("opp 4 streak")
            ##print((-10)**(n+4))
            return -10**(n+3)
        running_sum = running_sum + my_list[0]*10**(n+3)
        # ###print(my_list)
       	for i in range(1, n-1):
       		running_sum += my_list[i] * 10**(n-i)  #STILL TRYING TO IMPLEMENT CORRECT THINGY

       	for i in range(1, n-1):
       		opp_sum += opp_list[i] * 10**(n-i)  #STILL TRYING TO IMPLEMENT CORRECT THINGY

        ##print("no 4 streak")
        #print(running_sum- opp_sum)
        #print("----------------")
        return (running_sum - opp_sum)

def gameIsOver(state, curr_player_token):
    if curr_player_token == "R":
        opp_token = "Y"
    else:
        opp_token = "R"

    if  find_streak(state, curr_player_token , state["connect_n"]) >= 1:
        return True
    elif find_streak(state, opp_token, state["connect_n"]) >= 1:
        return True
    else:
        return False

def find_streak(state, token, streak):
    """
    Search streaks of a token in the grid
    :param grid: a grid of connect four
    :param token: token of a player
    :param streak: number of consecutive "token"
    :return count: number of streaks founded
    """
    count = 0
    # ##print("FINDING STREAKS:")
    # ##print(streak)
    # ##print("-----------------")
    grid = state["board"]
    # for each box in the grid...
    for i in range(0, state["columns"]):
        for j in range(0, len(state["board"][i])):
            # ...that is of the token we're looking for...
            if grid[i][j] == token:
                # check if a vertical streak starts at index [i][j] of the grid game
                count += find_vertical_streak(i, j, state, streak)

                # check if a horizontal streak starts at index [i][j] of the grid game
                count += find_horizontal_streak(i, j, state, streak)

                # check if a diagonal streak starts at index [i][j] of the grid game
                count += find_diagonal_streak(i, j, state, streak)
    # return the sum of streaks of length 'streak'

    return count

def find_horizontal_streak(col, row, state, streak):
    """
    Search vertical streak starting at index [col][row] in the grid
    :param col: col the grid
    :param row: rowumn of the grid
    :param grid: a grid of connect four
    :param streak: number of "token" consecutive
    :return: 0: no streak found, 1: streak founded
    """
    grid = state["board"]
    consecutive_count = 0

	#if col + streak - 1 < CONNECT_FOUR_GRID_HEIGHT:
    for i in range(0, streak):
        if (col + i) >= state["columns"] or row >= len (state["board"][col + i]):
            break
        if grid[col][row] == grid[col + i][row]:
            consecutive_count += 1
        else:
            break

    if consecutive_count == streak:
        return 1
    else:
        return 0

def find_vertical_streak(col, row, state, streak):
    """
    Search horizontal streak starting at index [col][row] in the grid
    :param col: col the grid
    :param row: rowumn of the grid
    :param grid: a grid of connect four
    :param streak: number of "token" consecutive
    :return: 0: no streak found, 1: streak founded
    """
    grid = state["board"]
    consecutive_count = 0

    for i in range(0, streak):
        if row + i >= len (state["board"][col]):
            break
        if grid[col][row] == grid[col][row + i]:
            consecutive_count += 1
        else:
            break

    if consecutive_count == streak:
        return 1
    else:
        return 0

def find_diagonal_streak(col, row, state, streak):
    """
    Search diagonal streak starting at index [col][row] in the grid
    It check positive and negative slope
    :param col: col the grid
    :param row: rowumn of the grid
    :param grid: a grid of connect four
    :param streak: number of "token" consecutive
    :return total: number of streaks founded
    """
    total = 0
    grid = state["board"]
    w = state["columns"] -1
    # check for diagonals with positive slope
    consecutive_count = 0
    #if col + streak - 1 < CONNECT_FOUR_GRID_HEIGHT and
    if row + streak - 1 < w:
        for i in range(0, streak):
            if (col + i) >= state["columns"] or row + i >= len (state["board"][col+i]):
                break
            if grid[col][row] == grid[col + i][row + i]:
                consecutive_count += 1
            else:
                break

    if consecutive_count == streak:
        total += 1

    # check for diagonals with negative slope
    consecutive_count = 0
    if col - streak + 1 >= 0 and row + streak - 1 < w:
        for i in range(0, streak):
            if (col - i) < 0 or row + i >= len (state["board"][col-i]):
                break
            if grid[col][row] == grid[col - i][row + i]:
                consecutive_count += 1
            else:
                break

    if consecutive_count == streak:
        total += 1

    return total

def get_connect_move(state):
    move = my_best_move(state)
    return {
        "move": move,
        "team-code": state["team-code"]
    }

def print_board(state):
    grid = state["board"]
    largest_height = 0
    for i in grid:
        if len(i) > largest_height:
            largest_height = len(i)

    for x in range(largest_height-1, -1, -1):
        for y in range(0,state["columns"]):
            if x < len(grid[y]):
                print (grid[y][x], end="", flush=True)
            else:
                print (" ", end="", flush=True)
            print (" | ", end="", flush=True)
        print("")
        print("---------------------------")

    for a in range (0, state["columns"]):
        print(a, end="", flush=True)
        print (" | ", end="", flush=True)
    print("")

def make_move(move, token):
    test_state["board"][move].append(token)

def get_move(state):
    if state["game"] == "chicken":
        return get_chicken_move(state)

    if state["game"] == "connect_more":
        return get_connect_move(state)

#print (get_move(state))

# if __name__ == '__main__':
#     test_state = {
#         "team-code": "eef8976e",
#         "game": "connect_more",
#         "opponent-name": "mighty_ducks",
#         "columns": 6,
#         "connect_n": 4,
#         "your-token": "R",
#         "board": [
#             ["Y"],
#             [],
#             [],
#             [],
#             [],
#             [],
#         ]
#     }
#     while(True):
#         make_move(get_move(test_state)["move"], "R")
#         if find_streak(test_state,"R",test_state["connect_n"]):
#             print("COMPUTER BEAT U ")
#             print_board(test_state)
#             break
#         print_board(test_state)
#         print("-------------------------")
#         human_move = int(input("Make A Move: "))
#         make_move(human_move, "Y")
#         if  find_streak(test_state,"Y",test_state["connect_n"]):
#             print("HUMAN WINS!!! ")
#             print_board(test_state)
#             break
#     random.seed(time.time())
#     state = {
#         "game": "chicken",
#         "opponent-name": "the_baddies",
#         "team-code": "abcd",
#         "prev-response-time": None,
#         "last-opponent-play": None,
#         "last-outcome": None
#     }
#     mean = random.random() * 4 
#     std = random.random() * 1
#     print(("Distribution has mean %f and std %f") % (mean, std))
#     reaction_times = numpy.random.normal(mean, std, 100)
#     your_score = 0
#     opp_score = 0
#     wins = 0
#     losses = 0
#     crashes = 0
#     ties = 0
#     reacs = [] 
#     sig_to_use = 1.25
#     for i in range(100):
#         if i % 10 == 0:
#             state['opponent-name'] += "a"
#             sig_to_use = (1.0 * random.randint(100, 400))/100.
#             print("using sigma %f" % sig_to_use)
#         print(("Round %d") % i)
#         the_move = get_move(state)["move"]
#         reac_time = reaction_times[i]
#         if reac_time > 10:
#             reac_time = 10
#         if reac_time < 0:
#             reac_time = 0
#         rand_move = 10
#         if len(reacs) > 6:
#             opp_mean, opp_std = get_stats(reacs)
#             rand_move = opp_mean + sig_to_use*opp_std
#         your_s = 0
#         rand_s = 0
#         state["prev-response-time"] = reac_time
#         state["last-opponent-play"] = rand_move
#         print(("Your move was %f") % the_move)
#         print(("Opp move was %f") % rand_move)
#         print(("Reaction time was %f") % reac_time)
#         if rand_move < reac_time and the_move < reac_time:
#             your_s = -10
#             rand_s = -10
#             crashes += 1
#             print("You crashed!")
#         elif rand_move < the_move:
#             your_s = -1
#             rand_s = 1
#             losses += 1
#             print("You lost!")
#         elif the_move < rand_move:
#             your_s = 1
#             rand_s = -1
#             wins += 1
#             print("You won!")
#         else:
#             ties += 1
#             print("Tie")
#         state["last-outcome"] = your_s
#         your_score += your_s
#         opp_score += rand_s
#         print(("YOUR SCORE: %d") % your_score)
#         print(("OPPO SCORE: %d") % opp_score)
#         print(("Crashes: %d, Losses:  %d, Wins: %d, Ties: %d") % (crashes, losses, wins, ties))
#         print("")
#         reacs.append(reac_time)
#     print(("Distribution has mean %f and std %f") % (mean, std))

import random
import json
import os.path
import time

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
    if state["prev-response-time"] is not None:
        info.setdefault("response-times", []).append(state["prev-response-time"])
    # example for storing previous response times
    if state["last-opponent-play"] is not None:
        info.setdefault("opponents",{}).setdefault(state["opponent-name"],[]).append(state["last-opponent-play"])
    move = 10
    if "response-times" in info.keys() and len(info["response-times"]) > 10:
        mean, std = get_stats(info["response-times"])
        # print(("Think that mean %f std %f") % (mean, std))
        move = min(mean + 1.29 * std,10)
    info.setdefault("moves", []).append(move)
    if state["last-outcome"] is not None:
        info.setdefault("outcomes", []).append(state["last-outcome"])
    save_info(info)
    return {
        "move": move,
        "team-code": state["team-code"],
    }

def valid_add(col, state): #Checks to see if the passed col adds to the previous state, returns largest valid integer after Checks
#assume column selected is added, look at all possible moves around it to see if there are openings for n sequentmyl states, if so, this is valid. Find the largest such int and return it
    cur_col = col
    height = len(state["board"][col-1]) + 1
    cur_height = height
    player = state["your-token"]
    cur_space = player
    best_move = 1
    cur_move = 1
    right_dag = 0 # 1 + 4
    left_dag = 0 # 3 + 6
    horz = 0 # 2 + 5
    closed = False
    for x in range (1,5):
        if x is 1:
            while cur_space is player:
                cur_height = cur_height - 1
                cur_col = cur_col - 1
                if cur_height < 1 or cur_col < 1:
                    closed = True
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'
                        closed = True

            cur_space = player
            cur_height = height
            cur_col = col

            while cur_space is player:
                cur_height = cur_height + 1
                cur_col = cur_col + 1
                if cur_height < 1 or cur_col > state["columns"]:
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    closed = False
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'

        if cur_move >= state["connect_n"]:
            return cur_move

        if cur_move > best_move and closed is not True:
            best_move = cur_move

        cur_move = 1
        cur_space = player
        cur_height = height
        cur_col = col
        closed = False

        if x is 2:
            while cur_space is player:
                cur_col = cur_col - 1
                if cur_height < 1 or cur_col < 1:
                    closed = True
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'
                        closed = True

            cur_space = player
            cur_height = height
            cur_col = col

            while cur_space is player:
                cur_col = cur_col + 1
                if cur_height < 1 or cur_col > state["columns"]:
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    closed = False
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'

        if cur_move >= state["connect_n"]:
            return cur_move
        if cur_move > best_move and closed is not True:
            best_move = cur_move

        cur_move = 1
        cur_space = player
        cur_height = height
        cur_col = col

        if x is 3:
            while cur_space is player:
                cur_height = cur_height + 1
                cur_col = cur_col - 1
                if cur_height < 1 or cur_col < 1:
                    closed = True
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'
                        closed = True

            cur_space = player
            cur_height = height
            cur_col = col

            while cur_space is player:
                cur_height = cur_height - 1
                cur_col = cur_col + 1
                if cur_height < 1 or cur_col > state["columns"]:
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    closed = False
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'O'

        if cur_move >= state["connect_n"]:
            return cur_move

        if cur_move > best_move and closed is not True:
            best_move = cur_move

        cur_move = 1
        cur_space = player
        cur_height = height
        cur_col = col

        if x is 4:
            while cur_space is player:
                cur_height = cur_height - 1
                if cur_height < 1:
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'O'
        if cur_move > best_move:
            best_move = cur_move

    return best_move

def opponent_check(col, state):
    cur_col = col
    height = len(state["board"][col-1]) + 1
    cur_height = height
    player = None
    if state["your-token"] is "R":
        player = "Y"
    else:
        player = "R"
    cur_space = player
    best_move = 1
    cur_move = 1
    right_dag = 0 # 1 + 4
    left_dag = 0 # 3 + 6
    horz = 0 # 2 + 5
    closed = False
    for x in range (1,5):
        if x is 1:
            while cur_space is player:
                cur_height = cur_height - 1
                cur_col = cur_col - 1
                if cur_height < 1 or cur_col < 1:
                    closed = True
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'
                        closed = True

            cur_space = player
            cur_height = height
            cur_col = col

            while cur_space is player:
                cur_height = cur_height + 1
                cur_col = cur_col + 1
                if cur_height < 1 or cur_col > state["columns"]:
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    closed = False
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'

        if cur_move >= state["connect_n"]:
            return cur_move

        if cur_move > best_move and closed is not True:
            best_move = cur_move

        cur_move = 1
        cur_space = player
        cur_height = height
        cur_col = col
        closed = False

        if x is 2:
            while cur_space is player:
                cur_col = cur_col - 1
                if cur_height < 1 or cur_col < 1:
                    closed = True
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'
                        closed = True

            cur_space = player
            cur_height = height
            cur_col = col

            while cur_space is player:
                cur_col = cur_col + 1
                if cur_height < 1 or cur_col > state["columns"]:
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    closed = False
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'

        if cur_move >= state["connect_n"]:
            return cur_move
        if cur_move > best_move and closed is not True:
            best_move = cur_move

        cur_move = 1
        cur_space = player
        cur_height = height
        cur_col = col

        if x is 3:
            while cur_space is player:
                cur_height = cur_height + 1
                cur_col = cur_col - 1
                if cur_height < 1 or cur_col < 1:
                    closed = True
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'opponent'
                        closed = True

            cur_space = player
            cur_height = height
            cur_col = col

            while cur_space is player:
                cur_height = cur_height - 1
                cur_col = cur_col + 1
                if cur_height < 1 or cur_col > state["columns"]:
                    break
                elif len(state["board"][cur_col-1]) < cur_height:
                    closed = False
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'O'

        if cur_move >= state["connect_n"]:
            return cur_move

        if cur_move > best_move and closed is not True:
            best_move = cur_move

        cur_move = 1
        cur_space = player
        cur_height = height
        cur_col = col

        if x is 4:
            while cur_space is player:
                cur_height = cur_height - 1
                if cur_height < 1:
                    break
                else:
                    if state["board"][cur_col-1][cur_height-1] is player:
                        cur_space = player
                        cur_move = cur_move + 1
                    else:
                        cur_space = 'O'
        if cur_move > best_move:
            best_move = cur_move

    return best_move


def get_connect_move(state):
    my_best_move = 1
    my_best_column = 1
    opp_best_move = 1
    opp_best_column = 1
    for x in range(1, state["columns"]+1):
        temp = valid_add(x, state)
        opp_temp = opponent_check(x, state)
        if temp > my_best_move:
            my_best_move = temp
            my_best_column = x

        if opp_temp > opp_best_move:
            opp_best_move = opp_temp
            opp_best_column = x

    if my_best_move >= opp_best_move:
        return {
            "move": my_best_column-1,  # Column in which you will move (create mark "your-token")
            "team-code": state["team-code"]  # Must match the code received in the state object
        }


    return {
        "move": opp_best_column-1,  # Column in which you will move (create mark "your-token")
        "team-code": state["team-code"]  # Must match the code received in the state object
    }

#----------------------------------------new stuff ------------------------------- (weren't able to get it working in time)
#
# def my_best_move(state):
#         # timer for testing
#         start_time = int(round(time.time() * 1000))
#         # determine opponent's token
#         if state["your-token"] is 'R':
#             opp_token = 'Y'
#         else:
#             opp_token = 'R'
#
#         # enumerate all legal moves
#         # will map legal move states to their alpha values
#         valid_moves = {}
#         # check if the move is legal for each column
#         for col in range(0, state["columns"]):
#             # simulate the move in column `col` for the current player
#             # tmp_state = simulate_move(state, col, state["your-token"])
#             valid_moves[col] = -find(0, state, state["your-token"])
#
#         best_alpha = -99999999
#         best_move = None
#         moves = valid_moves.items()
#         print(moves)
#         # search the best "move" with the highest `alpha` value
#         for move, alpha in moves:
#             if alpha >= best_alpha:
#                 best_alpha = alpha
#                 best_move = move
#
#         end_time = int(round(time.time() * 1000))
#         print ("response time: ", (end_time - start_time))
#
#         return best_move
#
#
# def find(depth, state, curr_player_token):
#     print("trying to find")
#     # enumerate all legal moves from this state
#     legal_moves = []
#     for i in range(0,state["columns"]):
#         # simulate the move in column i for curr_player
#         tmp_state = simulate_move(state, i, curr_player_token)
#         legal_moves.append(tmp_state)
#
#     if depth == 0 or len(legal_moves) == 0:
#         # return the heuristic value of node
#         print(eval_game(depth, state, curr_player_token))
#         return eval_game(depth, state, curr_player_token)
#
#     # determine opponent's token
#     if curr_player_token is "R":
#         opp_player_token = "Y"
#     else:
#         opp_player_token = "R"
#
#     alpha = -99999999
#     for child in legal_moves:
#         if child == None:
#             print("child == None (search)")
#         alpha = max(alpha, -find(depth - 1, child, opp_player_token)) #why are we passing in opp_player token each time? then it changes at each recursive step
#     print(alpha)
#     return alpha
#
#
# def simulate_move(state, column, token):
#     """
#     Simulate a "move" in the grid `grid` by the current player with its token `token.
#     :param grid: a grid of connect four
#     :param column: column index
#     :param token: token of a player
#     :return tmp_grid: the new grid with the "move" just added
#     """
#     #redraw the board here
#     tmp_state = state
#     tmp_state["board"][column].append(token)
#     return tmp_state
#
#
# def eval_game(depth, state, curr_player_token):
#         #This is where you can use my code (have to change how the counter works to count the streaks)
#         if curr_player_token == "R":
#             opp_token = "Y"
#         else:
#             opp_token = "R"
#         # get scores of human and my player with theirs streaks
#         n = state["connect_n"]
#         my_list = []
#         for i in range(2, n+1):
#         	my_list.append(find_streak(state, curr_player_token, i))
#        	opp_list = []
#
#        	for j in range(2, n+1):
#        		opp_list.append(find_streak(state, opp_token, j))
#
#        	running_sum = 0
#         opp_sum = 0
#        	my_list.reverse()
#        	opp_list.reverse()
#         if opp_list[0] > 0:
#         	return -10^(n+4) - depth
#         running_sum = running_sum + my_list[0]*10^(n+2)
#         # print(my_list)
#        	for i in range(1, n-1):
#        		running_sum += my_list[i] * 10^(n-i)  #STILL TRYING TO IMPLEMENT CORRECT THINGY
#
#        	for i in range(1, n-1):
#        		opp_sum += opp_list[i] * 10^(n-i)  #STILL TRYING TO IMPLEMENT CORRECT THINGY
#
#         print(my_list)
#         print(opp_list)
#
#         return (running_sum - opp_sum + depth)
#
#
# def find_streak(state, token, streak):
#     """
#     Search streaks of a token in the grid
#     :param grid: a grid of connect four
#     :param token: token of a player
#     :param streak: number of consecutive "token"
#     :return count: number of streaks founded
#     """
#     count = 0
#     grid = state["board"]
#     # for each box in the grid...
#     for i in range(0, state["columns"]):
#         for j in range(0, len(state["board"][i])):
#             # ...that is of the token we're looking for...
#             if grid[i][j] == token:
#                 # check if a vertical streak starts at index [i][j] of the grid game
#                 count += find_vertical_streak(i, j, state, streak)
#
#                 # check if a horizontal streak starts at index [i][j] of the grid game
#                 count += find_horizontal_streak(i, j, state, streak)
#
#                 # check if a diagonal streak starts at index [i][j] of the grid game
#                 count += find_diagonal_streak(i, j, state, streak)
#     # return the sum of streaks of length 'streak'
#
#     return count
#
# def find_horizontal_streak(row, col, state, streak):
#     """
#     Search vertical streak starting at index [row][col] in the grid
#     :param row: row the grid
#     :param col: column of the grid
#     :param grid: a grid of connect four
#     :param streak: number of "token" consecutive
#     :return: 0: no streak found, 1: streak founded
#     """
#     grid = state["board"]
#     consecutive_count = 0
#
# 	#if row + streak - 1 < CONNECT_FOUR_GRID_HEIGHT:
#     for i in range(0, streak):
#         if (row + i) >= state["columns"] or col >= len (state["board"][row + i]):
#             break
#         if grid[row][col] == grid[row + i][col]:
#             consecutive_count += 1
#         else:
#             break
#
#     if consecutive_count == streak:
#         return 1
#     else:
#         return 0
#
# def find_vertical_streak(row, col, state, streak):
#     """
#     Search horizontal streak starting at index [row][col] in the grid
#     :param row: row the grid
#     :param col: column of the grid
#     :param grid: a grid of connect four
#     :param streak: number of "token" consecutive
#     :return: 0: no streak found, 1: streak founded
#     """
#     grid = state["board"]
#     w = state["columns"] -1
#
#     consecutive_count = 0
#     if col + streak - 1 < w:
#         for i in range(0, streak):
#             if (row + i) >= state["columns"] or col + i >= len (state["board"][row]):
#                 break
#             if grid[row][col] == grid[row][col + i]:
#                 consecutive_count += 1
#             else:
#                 break
#
#     if consecutive_count == streak:
#         return 1
#     else:
#         return 0
#
# def find_diagonal_streak(row, col, state, streak):
#     """
#     Search diagonal streak starting at index [row][col] in the grid
#     It check positive and negative slope
#     :param row: row the grid
#     :param col: column of the grid
#     :param grid: a grid of connect four
#     :param streak: number of "token" consecutive
#     :return total: number of streaks founded
#     """
#     total = 0
#     grid = state["board"]
#     w = state["columns"] -1
#     # check for diagonals with positive slope
#     consecutive_count = 0
#     #if row + streak - 1 < CONNECT_FOUR_GRID_HEIGHT and
#     if col + streak - 1 < w:
#         for i in range(0, streak):
#             if (row + i) >= state["columns"] or col + i >= len (state["board"][row+i]):
#                 break
#             if grid[row][col] == grid[row + i][col + i]:
#                 consecutive_count += 1
#             else:
#                 break
#
#     if consecutive_count == streak:
#         total += 1
#
#     # check for diagonals with negative slope
#     consecutive_count = 0
#     if row - streak + 1 >= 0 and col + streak - 1 < w:
#         for i in range(0, streak):
#             if (row - i) < 0 or col + i >= len (state["board"][row-i]):
#                 break
#             if grid[row][col] == grid[row - i][col + i]:
#                 consecutive_count += 1
#             else:
#                 break
#
#     if consecutive_count == streak:
#         total += 1
#
#     return total
#
# # def __winpositions(lines, player):
# #     lines = __winlines(player)
# #     winpositions = {}
# #     for line in lines:
# #         pieces = 0
# #         empty = None
# #         for x, y in line:
# #             if state["board"][x][y] == player:
# #                 pieces = pieces + 1
# #             elif state["board"][x][y] == "":
# #                 if not empty == None:
# #                     break
# #                 empty = (x, y)
# #         if pieces == 3:
# #             winpositions["{0},{1}".format(x, y)] = True
# #     return winpositions
# #
# # def __winlines(player):
# #     lines = []
# #     # horizontal
# #     for y in range(height):
# #         winning = []
# #         for x in range(width):
# #             pos = state["board"][x][y]      #THIS LINE WILL CAUSE THE PROGRAM TO CRASH BECAUSE YOU CAN'T ACCESS THE LIST IF ITS NOT POPULATED
# #             if pos == player or  pos == "":
# #                 winning.append((x,y))
# #                 if len(winning) >= n:
# #                     lines.append(winning[-n:])
# #                 else:
# #                     winning = []
# #     # vertical
# #
# #     for x in range(width):
# #       winning = []
# #       for y in range(height):
# #           pos = state["board"][x][y]
# #           if pos == player or pos == "":
# #               winning.append((x,y))
# #               if len(winning) >= n:
# #                 lines.append(winning[-n:])
# #               else:
# #                 winning = []
# #
# #     # diagonal
# #     winning = []
# #     for cx in range(width-1):
# #       sx,sy = max(cx-2,0),abs(min(cx-2,0))
# #       winning = []
# #       for cy in range(height):
# #         x,y = sx+cy,sy+cy
# #         if x<0 or y<0 or x>=width or y>=height:
# #           continue
# #         if state["board"][x][y] == player or state["board"][x][y] == "":
# #           winning.append((x,y))
# #           if len(winning) >= n:
# #             lines.append(winning[-n:])
# #         else:
# #           winning = []
# #
# #
# #     # other diagonal
# #     winning = []
# #     for cx in range(width-1):
# #       sx,sy = width-1-max(cx-2,0),abs(min(cx-2,0))
# #       winning = []
# #       for cy in range(height):
# #         x,y = sx-cy,sy+cy
# #         if x<0 or y<0 or x>=width or y>=height:
# #           continue
# #         if state["board"][x][y] == player or state["board"][x][y] == "":
# #           winning.append((x,y))
# #           if len(winning) >= n:
# #             lines.append(winning[-n:])
# #         else:
# #           winning = []
# #     # return
# #     return lines
#
# def get_move(state):
#     # Your code can be called from here however you like
#     # You are allowed the use of load_data() and save_data(info)
#     # info = load_data()
#
#     # num_columns = state["columns"] #number of columns (since there's no roof)
#     # num = state["connect_n"] #number we have to connect in a row
#     #
#     # player = state["your-token"] #Either "R" or "B"
#     # if (player == "R"):
#     #     opponent = "Y"
#     # else:
#     #     opponent = "R"
#     #
#     # print(state["board"])
#     # h = 0 #initmylizing height h
#     # print ("----------------")
#     # print(state["board"][1])
#     # print(valid_add(3, state))
#     # print("-------------")
#     # print(opponent_check(6,state))
#     #
#     # for i in range(num_columns): #choosing the height to go up to, since we dont want to add infinite spots going up, its good to have an upper bound on the board
#     #     col = len(state["board"][i])
#     #     if h < col:
#     #         h = col
#     #
#     # set_vars(h, num_columns, player, num) #setter for the global varmybles so other functions can use them
#     #
#     # # But you must return a valid move that looks like the following:
#     # return {
#     #     "move": 2,  # Column in which you will move (create mark "your-token")
#     #     "team-code": "eef8976e"  # Must match the code received in the state object
#     # }
#     move = my_best_move(state)
#     return {
#         "move": move,
#         "team-code": state["team-code"]
#     }

def get_move(state):
    if state["game"] == "chicken":
        return get_chicken_move(state)

    if state["game"] == "connect_more":
        return get_connect_move(state)

#print (get_move(state))

# if __name__ == '__main__':
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
#     for i in range(100):
#         print(("Round %d") % i)
#         the_move = get_move(state)["move"]
#         reac_time = reaction_times[i]
#         if reac_time > 10:
#             reac_time = 10
#         if reac_time < 0:
#             reac_time = 0
#         rand_move = random.random() * 10
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
#     print(("Distribution has mean %f and std %f") % (mean, std))

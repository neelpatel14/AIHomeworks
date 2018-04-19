import time
import copy

TEAM_NAME = "ani and friends"
MEMBERS = ["np2ch", "ar9fh", "aml5ha"]  # Include a list of your members’ UVA IDs

test_state = {
    "team-code": "eef8976e",
    "game": "connect_more",
    "opponent-name": "mighty_ducks",
    "columns": 7,
    "connect_n": 4,
    "your-token": "R",
    "board": [
        [],
        [],
        [],
        [],
        [],
        [],
	    [],
    ]
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

def get_move(state):
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

while( True):
    make_move(get_move(test_state)["move"], "R")
    if find_streak(test_state,"R",test_state["connect_n"]):
        print("COMPUTER BEAT U ")
        print(print_board)
        break
    print_board(test_state)
    print("-------------------------")
    human_move = int(input("Make A Move: "))
    make_move(human_move, "Y")
    if  find_streak(test_state,"Y",test_state["connect_n"]):
        print("HUMAN WINS!!! ")
        print(print_board(test_state))
        break

TEAM_NAME = "ani and friends"
MEMBERS = ["np2ch", "ar9fh", "aml5ha"]  # Include a list of your members’ UVA IDs

height = 0
width = 0
n = 0
player = "a"

state = {
    "team-code": "eef8976e",
    "game": "connect_more",
    "opponent-name": "mighty_ducks",
    "columns": 6,
    "connect_n": 5,
    "your-token": "R",
    "board": [
        ["R", "Y"],
        ["R"],
        [],
        ["R", "Y", "Y", "Y"],
        ["Y", "Y"],
        [],
    ]
}


def set_vars(h, w, p, num):
    height = h
    width = w
    player = p
    n = num


def valid_add(col, state): #Checks to see if the passed col adds to the previous state, returns largest valid integer after Checks
#assume column selected is added, look at all possible moves around it to see if there are openings for n sequential states, if so, this is valid. Find the largest such int and return it
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

    if my_best_move > opp_best_move:
        return {
            "move": my_best_column,  # Column in which you will move (create mark "your-token")
            "team-code": "eef8976e"  # Must match the code received in the state object
        }


    return {
        "move": opp_best_column,  # Column in which you will move (create mark "your-token")
        "team-code": "eef8976e"  # Must match the code received in the state object
    }

def get_move(state):
    # Your code can be called from here however you like
    # You are allowed the use of load_data() and save_data(info)
    # info = load_data()


    num_columns = state["columns"] #number of columns (since there's no roof)
    num = state["connect_n"] #number we have to connect in a row

    player = state["your-token"] #Either "R" or "B"
    if (player == "R"):
        opponent = "Y"
    else:
        opponent = "R"

    print(state["board"])
    h = 0 #initializing height h
    print ("----------------")
    print(state["board"][1])
    print(valid_add(3, state))
    print("-------------")
    print(opponent_check(6,state))

    for i in range(num_columns): #choosing the height to go up to, since we dont want to add infinite spots going up, its good to have an upper bound on the board
        col = len(state["board"][i])
        if h < col:
            h = col

    set_vars(h, num_columns, player, num) #setter for the global variables so other functions can use them

    # But you must return a valid move that looks like the following:
    return {
        "move": 2,  # Column in which you will move (create mark "your-token")
        "team-code": "eef8976e"  # Must match the code received in the state object
    }

print(get_connect_move(state))


def __winpositions(lines, player):
    lines = __winlines(player)
    winpositions = {}
    for line in lines:
        pieces = 0
        empty = None
        for x, y in line:
            if state["board"][x][y] == player:
                pieces = pieces + 1
            elif state["board"][x][y] == "":
                if not empty == None:
                    break
                empty = (x, y)
        if pieces == 3:
            winpositions["{0},{1}".format(x, y)] = True
    return winpositions

def __winlines(player):
    lines = []
    # horizontal
    for y in range(height):
        winning = []
        for x in range(width):
            pos = state["board"][x][y]      #THIS LINE WILL CAUSE THE PROGRAM TO CRASH BECAUSE YOU CAN'T ACCESS THE LIST IF ITS NOT POPULATED
            if pos == player or  pos == "":
                winning.append((x,y))
                if len(winning) >= n:
                    lines.append(winning[-n:])
                else:
                    winning = []
    # vertical

    for x in range(width):
      winning = []
      for y in range(height):
          pos = state["board"][x][y]
          if pos == player or pos == "":
              winning.append((x,y))
              if len(winning) >= n:
                lines.append(winning[-n:])
              else:
                winning = []

    # diagonal
    winning = []
    for cx in range(width-1):
      sx,sy = max(cx-2,0),abs(min(cx-2,0))
      winning = []
      for cy in range(height):
        x,y = sx+cy,sy+cy
        if x<0 or y<0 or x>=width or y>=height:
          continue
        if state["board"][x][y] == player or state["board"][x][y] == "":
          winning.append((x,y))
          if len(winning) >= n:
            lines.append(winning[-n:])
        else:
          winning = []


    # other diagonal
    winning = []
    for cx in range(width-1):
      sx,sy = width-1-max(cx-2,0),abs(min(cx-2,0))
      winning = []
      for cy in range(height):
        x,y = sx-cy,sy+cy
        if x<0 or y<0 or x>=width or y>=height:
          continue
        if state["board"][x][y] == player or state["board"][x][y] == "":
          winning.append((x,y))
          if len(winning) >= n:
            lines.append(winning[-n:])
        else:
          winning = []
    # return
    return lines

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
        ["R", ],
        ["Y", "Y"],
        [],
    ]
}


def set_vars(h, w, p, num):
    height = h
    width = w
    player = p
    n = num


def get_move(state):
    # Your code can be called from here however you like
    # You are allowed the use of load_data() and save_data(info)
    # info = load_data()


    num_columns = state["columns"]
    num = state["connect_n"]

    player = state["your-token"]
    if (player == "R"):
        opponent = "B"
    else:
        opponent = "R"

    print(state["board"])
    h = 0



    for i in range(num_columns):
        col = len(state["board"][i])
        if h < col:
            h = col

    set_vars(h, num_columns, player, num)

    # But you must return a valid move that looks like the following:
    return {
        "move": 2,  # Column in which you will move (create mark "your-token")
        "team-code": "eef8976e"  # Must match the code received in the state object
    }

get_move(state)


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

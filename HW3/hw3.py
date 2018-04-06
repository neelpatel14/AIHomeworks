import random
import json
import os.path
import numpy
import time

TEAM_NAME = "ani and friends"

# this is a test state function for you to drive the following test case with
# NOTE: you will receive this when the game playing program calls your get_move
test_state = {
    "game": "chicken",
    "opponent-name": "the_baddies",
    "team-code": "abc123",
    "prev-response-time": 0.5,
    "last-opponent-play": 0.71,
    "last-outcome": -10,
}
info_filename = 'chicken_info.json'
info_json = {}

# This will load whatever dictionary you last saved, stub included to drive example,
#   isn't actual function
def load_info():
    info = {}
    if os.path.isfile(info_filename):
        with open(info_filename, 'r') as info_file:
            info = json.load(info_file)
    return info

# This will save (and overwrite) whatever dictionary you last saved
# Stub included to drive example, isn't actual function
def save_info(info):
    if state["game"] == "chicken":
        new_info = load_info()
        new_info.update(info)
        with open(info_filename, 'w') as info_file:
            json.dump(new_info, info_file)

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
    if "response-times" in info.keys() and len(info["response-times"]) > 5:
        mean, std = get_stats(info["response-times"])
        print(("Think that mean %f std %f") % (mean, std))
        move = min(mean + 0.84 * std,10)
    info.setdefault("moves", []).append(move)
    if state["last-outcome"] is not None:
        info.setdefault("outcomes", []).append(state["last-outcome"])
    save_info(info)
    return {
        "move": move,
        "team-code": state["team-code"],
    }


def get_connect_move(state):

    return {
        "move": random.randint(1,state["columns"]),
        "team-code": state["team-code"],
    }

def get_move(state):
    if state["game"] == "chicken":
        return get_chicken_move(state)

    if state["game"] == "connect_more":
        return get_connect_move(state)

#print (get_move(state))

if __name__ == '__main__':
    random.seed(time.time())
    state = {
        "game": "chicken",
        "opponent-name": "the_baddies",
        "team-code": "abcd",
        "prev-response-time": None,
        "last-opponent-play": None,
        "last-outcome": None
    }
    mean = random.random() * 10
    std = random.random() * 3
    print(("Distribution has mean %f and std %f") % (mean, std))
    reaction_times = numpy.random.normal(mean, std, 100)
    your_score = 0
    opp_score = 0
    wins = 0
    losses = 0
    crashes = 0
    ties = 0
    for i in range(100):
        print(("Round %d") % i)
        the_move = get_move(state)["move"]
        reac_time = reaction_times[i]
        if reac_time > 10:
            reac_time = 10
        if reac_time < 0:
            reac_time = 0
        rand_move = random.random() * 10
        your_s = 0
        rand_s = 0
        state["prev-response-time"] = reac_time
        state["last-opponent-play"] = rand_move
        print(("Your move was %f") % the_move)
        print(("Opp move was %f") % rand_move)
        print(("Reaction time was %f") % reac_time)
        if rand_move < reac_time and the_move < reac_time:
            your_s = -10
            rand_s = -10
            crashes += 1
            print("You crashed!")
        elif rand_move < the_move:
            your_s = -1
            rand_s = 1
            losses += 1
            print("You lost!")
        elif the_move < rand_move:
            your_s = 1
            rand_s = -1
            wins += 1
            print("You won!")
        else:
            ties += 1
            print("Tie")
        state["last-outcome"] = your_s
        your_score += your_s
        opp_score += rand_s
        print(("YOUR SCORE: %d") % your_score)
        print(("OPPO SCORE: %d") % opp_score)
        print(("Crashes: %d, Losses:  %d, Wins: %d, Ties: %d") % (crashes, losses, wins, ties))
        print("")
    print(("Distribution has mean %f and std %f") % (mean, std))

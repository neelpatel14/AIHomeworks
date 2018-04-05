import random
import json
import os.path

TEAM_NAME = "ani and friends"
MEMBERS = ["np2ch","ar9fh","aml5ha"] #Include a list of your members’ UVA IDs

# this is a test state function for you to drive the following test case with
# NOTE: you will receive this when the game playing program calls your get_move
state = {
	"game":	"chicken",
	"opponent-name": "the_baddies",
	"team-code": "abc123",
	"prev-response-time": 0.5,
	"last-opponent-play": 0.71,
	"last-outcome": -10,
}
info_filename = 'info.json'

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
    new_info = load_info()
    new_info.update(info)
    with open(info_filename, 'w') as info_file:
        json.dump(new_info, info_file)
"""
	if state["game"] == "chicken":
		#add new chicken info to old data

	if state["game"] =="connect_more":
		#add new connect_more data to old data
"""

# returns a random move (for sake of example)
def get_chicken_move(state):
	info = load_info() # info might be "{}" if first use, otherwise reads dictionary from your save file
	# example for storing previous response times
	if state["prev-response-time"] is not None:
		info.setdefault("opponents",{}).setdefault(state["opponent-name"],[]).append(state["prev-response-time"])
	save_info(info)
	return {
		"move": random.randint(0,10) * random.random(),
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
    print(load_info())
    save_info({'a': 2})

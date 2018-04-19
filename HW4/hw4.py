state = {
	"team-code": "eef8976e",
	"game": "sym",
	"opponent-name": "mighty-ducks",
	"prev-repetitions": 10, #Might be None if first game ever, or other number
	"last-opponent-play": 1, #0 or 1 depending on strategy played
	"last-outcome": 4, #Might be None if first game, or whatever outcome of play is
	"prospects": [
	[4,5],
	[3,2]
	]
}


def get_move(state):
	
	ans = {"team-code": "eef8976e", #identifying team by the code assigned by game-program
	"move": 1 #Can be 0 or 1 only
	}
	return ans


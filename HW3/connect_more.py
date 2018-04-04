TEAM_NAME = "ani and friends"
MEMBERS = ["np2ch","ar9fh","aml5ha"] #Include a list of your members’ UVA IDs

state = {
	"team-code": "eef8976e",
	"game": "connect_more",
	"opponent-name": "mighty_ducks",
	"columns": 6,
	"connect_n": 5,
	"your-token": "R",
	"board": [
	["R","Y"],
	["R"],
	[],
	["R",],
	["Y","Y"],
	[],
	]
}
def get_move(state):
	# Your code can be called from here however you like
	# You are allowed the use of load_data() and save_data(info)
	info = load_data()
	# But you must return a valid move that looks like the following:
	return {
		"move": 2, # Column in which you will move (create mark "your-token")
		"team-code": "eef8976e" # Must match the code received in the state object
	}
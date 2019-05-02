import requests

from obj.player import Player

"""
Game ID

- first 4 digits identify the season of the game (ie. 2017 for the 2017-2018 season).
- next 2 digits give the type of game, 
    where   01 = preseason 
            02 = regular season 
            03 = playoffs 
            04 = all-star
- final 4 digits identify the specific game number. 

For regular season and preseason games, this ranges from 0001 
to the number of games played. 
    - 1271 for seasons with 31 teams (2017 and onwards) 
    - 1230 for seasons with 30 teams

For playoff games:
    - 2nd digit of the specific number gives the round of the playoffs
    - 3rd digit specifies the matchup
    - 4th digit specifies the game (out of 7).
"""
game_id = '2018030213'

game_api_url = f"https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live?site=en_nhl"
shiftcharts_api_url = f"http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId={game_id}"

# get JSON data for game
game_JSON = requests.get(game_api_url).json()

# get JSON data for game shiftcharts
shiftcharts_JSON = requests.get(shiftcharts_api_url).json()

# get all players in the game
game_players = game_JSON["gameData"]["players"]

# init list to store Player objs
player_objs = []

# get dictionary containing player data and pass to Player constructor
for playerID in game_players:
    player_objs.append(Player(game_players[playerID]))

for player in player_objs:
    print(player.id)

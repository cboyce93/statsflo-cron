import requests

from obj.player import Player
from obj.play import Play

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
shifts = shiftcharts_JSON['data']

# get all players in the game
game_players = game_JSON["gameData"]["players"]

# init list to store Player objs
player_objs = {}

# get dictionary containing player data and pass to Player constructor

for player_args in game_players.items():
    kwargs = player_args[1]
    player_objs[kwargs['id']] = Player(kwargs)

# get all plays from game
all_plays = game_JSON["liveData"]["plays"]["allPlays"]

for playargs in all_plays:

    # create Play objs
    play = Play(playargs)
    eventID = play.result['eventTypeId'] # i.e., SHOT, BLOCKED SHOT etc.

    # shootouts excluded from player on-ice calcs
    if play.about['periodType'] != "SHOOTOUT":

        # Fenwick - any unblocked shot attempt (goals, shots on net and misses) outside of the shootout.
        # Corsi - Any shot attempt (goals, shots on net, misses and blocks) outside of the shootout.
        # Shots - any shot attempt on net (goals and shots on net) outside of the shootout.

        if "SHOT" in eventID or eventID == "GOAL":

            # set players on ice for play
            play.setPlayersOnIce(shifts)
            # update Player Corsi stats
            for playerID in play.players_on_ice:
                player_objs[playerID].update_corsi(play)

            # update Fenwick Corsi stats
            # blocked shots excluded
            if eventID != "BLOCKED_SHOT":
                for playerID in play.players_on_ice:
                    player_objs[playerID].update_fenwick(play)

            if eventID != "BLOCKED_SHOT" and eventID != "MISSED_SHOT":
                for playerID in play.players_on_ice:
                    player_objs[playerID].update_shots(play)

            if eventID == "GOAL":
                for playerID in play.players_on_ice:
                    player_objs[playerID].update_goals(play)




for playerID, player in player_objs.items():
    if player.all_CFP > 0:
        print(player.fullName, player.all_CF, player.all_CA, round(player.all_CFP, 2),
                               player.all_FF, player.all_FA, round(player.all_FFP,2),
                               player.all_SF, player.all_SA, round(player.all_SFP,2))


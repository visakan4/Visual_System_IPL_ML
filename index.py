from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
import GroundAnalysis
import PlayerAnalysis
import batsman_dismissal
import changeBattingCluster
import changeBowlingCluster
import bowlingEconomy
import no_of_wicket
import getPlayerInfo
import getTeamDetails

# initialising part
# adding configs for CORS support
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# testConnection
@app.route('/')
@cross_origin()
def test():
    return 'test index route'

# apiTest
@app.route('/api1')
@cross_origin()
def apifunc():
    return 'test api1'

# playerData
# param required - Player ID
# gets the batting strike rate, runs scored, average in every match, season_id, match_id of a player
# returns a json of playerDetails

@app.route('/playerData')
@cross_origin()
def playerAnalysis():
    playerId = request.args.get('playerId')
    return PlayerAnalysis.workFlow(playerId)

# searchPlayers
# gets all the player names and player id which will be used as drop down values in the select box.
# returns a json of list of available players

@app.route('/searchPlayers')
@cross_origin()
def searchPlayers():
    query = request.args.get('query')
    return PlayerAnalysis.getPlayers(query)

# batsmanDismissal
# get the number of times a player has got out in a specific manner. Details would be in season by season manner
# returns a json of number of times a player has got out

@app.route('/batsmanDismissal')
@cross_origin()
def dismissalPlayers():
    playerId = request.args.get('playerId')
    return batsman_dismissal.work_flow(int(playerId))

# bowlingClusterValues
# params - clusterCount, minBowlerEconomy, maxBowlerEconomy, minBowlingAverage, maxBowlingAverage
# get the new values to be clustered(Bowling)

@app.route('/bowlingClusterValues')
@cross_origin()
def getBowlingClusterValues():
    clusterCount = int(request.args.get('clusterCount'))
    minBowlerEconomy = int(request.args.get('minBowlerEconomy'))
    maxBowlerEconomy = int(request.args.get('maxBowlerEconomy'))
    minBowlingAverage = int(request.args.get('minBowlingAverage'))
    maxBowlingAverage = int(request.args.get('maxBowlingAverage'))
    return changeBowlingCluster.getBowlingCluster(clusterCount, minBowlerEconomy, maxBowlerEconomy, minBowlingAverage, maxBowlingAverage)


# battingClusterValues
# params - clusterCount, minBattingAverage, minStrikeRate, maxStrikeRate
# get the new values to be clusterd(Batting)

@app.route('/battingClusterValues')
@cross_origin()
def getBattingClusterValues():
    clusterCount = int(request.args.get('clusterCount'))
    minBattingAverage = int(request.args.get('minBattingAverage'))
    maxBattingAverage = int(request.args.get('maxBattingAverage'))
    minStrikeRate = int(request.args.get('minStrikeRate'))
    maxStrikeRate = int(request.args.get('maxStrikeRate'))
    return changeBattingCluster.getBattingCluster(clusterCount, minBattingAverage, maxBattingAverage, minStrikeRate, maxStrikeRate)

# bowlerEconomyRate
# param playerID
# returns a json which contains economy rate, nof of wickets, average taken by the player

@app.route('/bowlerEconomyRate')
@cross_origin()
def economyOfPlayers():
    playerId = request.args.get('playerId')
    return bowlingEconomy.getPlayerEconomy(int(playerId))

# wicketsCountCategory
# param playerID
# returns a json which contains details like no of wickets taken and no of wickets in a particular mode of dismissal

@app.route('/wicketsCountCategory')
@cross_origin()
def getWicketsPlayers():
    playerId = request.args.get('playerId')
    return no_of_wicket.getWicketCategoryCount(int(playerId))

# playerDetails
# param playerID
# returns json which contains player details like name, age, country, etc ...

@app.route('/playerDetails')
@cross_origin()
def getPlayerData():
    playerId = request.args.get('playerId')
    return getPlayerInfo.getPlayerDetails(int(playerId))

# TeamDetails
# returns json which contains runs scored by each team in each and every match

@app.route('/TeamDetails')
@cross_origin()
def getTeamDetails():
    return getTeamDetails.getMatchDetails()

# groundData
# returns a json which contains the win percentage of team playing first, second and teams winning toss in all the grounds

@app.route('/groundData')
@cross_origin()
def groundAnalysis():
    return GroundAnalysis.groundData()
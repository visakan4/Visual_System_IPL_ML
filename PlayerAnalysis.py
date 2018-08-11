import json
import pandas as ps

# getSeasonId
# param - match_id
# gets the season Id for a match

def getSeasonId(match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0], 'Season_Id']

# getYear
# param - match_id
# gets year in which the match took place

def getYear(match_id):
    return season_data.at[season_data[season_data['Match_Id'] == match_id].index[0],'Match_Date']

# isOut
# param - match_id, playerId
# returns true if the player has got out in the match, false otherwise

def isOut(match_id, playerId):
    out = False
    match_value = group_by_matches.get_group(match_id)
    player_value = match_value.groupby('Player_dissimal_Id')
    try:
        value = player_value.get_group(str(playerId))
        out = True
    except KeyError:
        out = False
    return out

# getAverage
# param - playerId
# Iterate through the striker Group and determine the number of runs scored by each player
# conditioning of data - Some instances had missing data. We have removed them as the number of instances were low and did not have much impact
# create a hash with details match_id, runs_scored_in_match, average, no_of_times_got_out, runs_scored, season_id, season_year
# push each hash into a array which would be converted into json

def getAverage(playerId):
    for name, group in strikerGroup:
        if (name == playerId):
            match_groups = group.groupby('Match_Id')
            no_of_out = 0
            runsScored = 0
            for match_id, match_group in match_groups:
                matchDetails = {}
                runsScored_in_match = 0
                for index, row in match_group.iterrows():
                    if not (row['Batsman_Scored'] == 'Do_nothing'):
                        if not (row['Batsman_Scored'] == ' '):
                            runsScored_in_match += int(row['Batsman_Scored'])
                            runsScored += int(row['Batsman_Scored'])
                if (isOut(match_id, playerId)):
                    no_of_out += 1
                if (no_of_out == 0):
                    average = runsScored
                else:
                    average = float(runsScored) / float(no_of_out)
                matchDetails['match_id'] = int(match_id)
                matchDetails['runs_scored_in_match'] = runsScored_in_match
                matchDetails['average'] = average
                matchDetails['no_of_times_got_out'] = no_of_out
                matchDetails['runs_scored'] = runsScored
                matchDetails['season_id'] = int(getSeasonId(match_id))
                matchDetails['season_year'] = getYear(match_id)
                playerDetails.append(matchDetails)

# workFlow
# parameter - PlayerID
# read the necessary files and creates the dataFrames
# groups the values based on matches and player id
# getAverage method is invoked
# converts the list of values into json
# returns the json

def workFlow(playerId):
    global ball_by_ball_data
    global season_data
    global playerDetails
    global strikerGroup
    global group_by_matches

    ball_by_ball_data = ps.read_csv(
        filepath_or_buffer='./indian-premier-league-csv-dataset/Ball_by_Ball.csv',
        sep=',')
    season_data = ps.read_csv(
        filepath_or_buffer='./indian-premier-league-csv-dataset/Match.csv', sep=',')

    playerDetails = []

    strikerGroup = ball_by_ball_data.groupby('Striker_Id')
    group_by_matches = ball_by_ball_data.groupby('Match_Id')
    getAverage(int(playerId))
    playerDetailsJSON = json.dumps(playerDetails)
    return (playerDetailsJSON)

# getPlayers
# create a has which would contain the player id and name of each player
# push each hash into array
# convert the final array into json

def getPlayers(query):
    dataSetFile = open("./indian-premier-league-csv-dataset/Player.csv", "r")
    myData = []
    for index, line in enumerate(dataSetFile):
        if index == 0:  # reading head
            head = line.replace("\r", "").replace("\n", "").split(",")  # \t for tab separated
        else:
            fields = line.replace("\r", "").replace("\n", "").split(",")
            fieldHashMap = {}
            for i, field in enumerate(fields):
                if head[i] in ["Player_Id", "Player_Name"]:
                    if head[i] == "Player_Id":
                        temp_id = field
                    if head[i] == "Player_Name":
                        if query in field.lower():
                            fieldHashMap['label'] = field
                            fieldHashMap['value'] = temp_id
                            myData.append(fieldHashMap)

    return json.dumps(myData)
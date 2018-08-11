import pandas as ps
import json

# readFiles
# read the player.csv as dataFrame and return the same

def readFiles():
    player_details = ps.read_csv(filepath_or_buffer='./indian-premier-league-csv-dataset/Player.csv',sep=',')
    return player_details

# getDetails
# param - player_details, player_id
# get the player name, age and country
# create a hash of the same
# return the json

def getDetails(player_details,player_id):
    detailshash = {}
    detailshash['name'] = player_details.at[player_details[player_details['Player_Id'] == player_id].index[0], 'Player_Name']
    detailshash['country'] = player_details.at[player_details[player_details['Player_Id'] == player_id].index[0], 'Country']
    detailshash['age'] = 2017 - int("19"+player_details.at[player_details[player_details['Player_Id'] == player_id].index[0], 'DOB'].split('-')[2])
    return detailshash

# getPlayerDetails
# param - player_id
# main method

def getPlayerDetails(player_id):
    player_details = readFiles()
    return (json.dumps(getDetails(player_details,player_id)))
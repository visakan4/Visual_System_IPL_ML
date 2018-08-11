import os
import csv
import json
import pandas as pd

# groundData
# read the necessary files, remove the headers
# convert the values into a dataFrame
# iterate through the dataFrame to determine the winner percentage
# calculate winning percentage on batting first, batting second
# calculate winning percentage on losing the toss and winning the toss

def groundData():
    script_dir = os.path.dirname("./indian-premier-league-csv-dataset/")
    fileName = "Match.csv"
    filePath = os.path.join(script_dir, fileName)
    file = open(filePath, "r")

    data = []

    for index, line in enumerate(file):
        if index == 0:
            header = line.replace("'", "").replace("\n", "").split(",")
        else:
            values = line.replace('"', "").replace("\n", "").split(",")
            if (len(values) > len(header)):
                temp = values
                values = []
                i = 0
                for value in temp:
                    if (i == 5):
                        values.append(temp[i] + " - " + temp[i + 1])
                        i += 2
                    elif (i == 7):
                        i += 1
                    else:
                        values.append(value)
                        i += 1
            hashValue = {}
            for i, value in enumerate(values):
                hashValue[header[i]] = value
            data.append(hashValue)

    processDataFrame = pd.DataFrame(data)

    groups = processDataFrame.groupby('Venue_Name')

    # a = processDataFrame['Venue_Name'].value_counts()

    analysisData = []
    jsonHeader = ['groundID', 'groundName', 'numberofMatchesPlayed', 'winPercentagePlayingFirst',
                  'winPercentagePlayingSecond', 'winPercentageWinningToss', 'winPercentageLosingToss']
    groupIndex = 0
    for name, group in groups:
        value = 0
        battingFirst = 0
        groundData = []
        groundHash = {}
        numberOfMatches = group.size / len(header)
        for index, row in group.iterrows():
            if (row['Match_Winner_Id'] == row['Toss_Winner_Id']):
                value += 1
            if ((row['Toss_Decision'] == 'bat') & (row['Toss_Winner_Id'] == row['Match_Winner_Id']) | (
                row['Toss_Decision'] == 'field') & (row['Toss_Winner_Id'] != row['Match_Winner_Id'])):
                battingFirst += 1
        groundData.append(groupIndex)
        groundData.append(name)
        groundData.append(numberOfMatches)
        groundData.append((float(battingFirst) / float(numberOfMatches)) * 100)
        groundData.append(((float(numberOfMatches) - float(battingFirst)) / float(numberOfMatches)) * 100)
        groundData.append((float(value) / float(numberOfMatches)) * 100)
        groundData.append(((float(numberOfMatches) - float(value)) / float(numberOfMatches)) * 100)
        for i, groundDataValue in enumerate(groundData):
            groundHash[jsonHeader[i]] = groundDataValue
        analysisData.append(groundHash)
        groupIndex += 1

    analysisJSON = json.dumps(analysisData)

    return analysisJSON


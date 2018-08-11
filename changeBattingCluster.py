import json
import numpy as np
from sklearn.cluster import KMeans
import warnings
from sklearn.preprocessing import normalize
from sklearn import metrics

# getBattingCluster
# initialise the values
# filter the value based on the selected values
# cluster the values
# return the new cluster values

def getBattingCluster(paramClusterCount, paramMinBattingAverage, paramMaxBattingAverage, paramMinStrikeRate, paramMaxStrikeRate):

    playerId = []
    playerName = []
    battingStrikeRate = []
    battingAverage = []
    ballsFaced = []
    ballsBowled = []
    totalDismissCount = []

    updatedId = []
    updatedStrikeRate = []
    updatedBattingAverage = []

    mainData = []

    averageBallFaced = 30

    cluster_count = paramClusterCount
    minBattingAverage = paramMinBattingAverage
    maxBattingAverage = paramMaxBattingAverage
    minStrikeRate = paramMinStrikeRate
    maxStrikeRate = paramMaxStrikeRate

    with open('./ClusterData/playerJsonData.json', 'r') as playerJson:
        jsonData = json.load(playerJson)
        for row in jsonData:
            playerId.append(row['player_id'])
            playerName.append(row['player_name'])
            battingStrikeRate.append(row['batting_strike_rate'])
            battingAverage.append(row['batting_average'])
            ballsFaced.append(row['balls_faced'])
            totalDismissCount.append(row['total_dismissal'])

    for i, indexaverage in enumerate(playerId):

        if battingAverage[i] >= minBattingAverage and battingAverage[i] <= maxBattingAverage:
            if battingStrikeRate[i] >= minStrikeRate and battingStrikeRate[i] <= maxStrikeRate:
                if ballsFaced[i] >= 30:
                    if battingStrikeRate[i] != 0 and battingAverage[i] != 0:
                        if totalDismissCount[i] > 6:
                            updatedId.append(playerId[i])
                            updatedStrikeRate.append(battingStrikeRate[i])
                            updatedBattingAverage.append(battingAverage[i])

    combinedData = np.vstack((updatedBattingAverage, updatedStrikeRate)).T
    battingNormalizedData = normalize(combinedData, axis=1, norm='l2')

    try:
        kmeanscluster = KMeans(n_clusters=cluster_count, random_state=0).fit(battingNormalizedData)

    except ValueError:
        print("ValueError encountered in batting cluster")

    km_labels = kmeanscluster.labels_

    print("Batting Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(battingNormalizedData, kmeanscluster.labels_, sample_size=1000))

    warnings.filterwarnings('ignore',
                            '.*Graph is not fully connected, spectral embedding.*',
                            UserWarning,
                            )

    batting_km_labels_list = km_labels.tolist()

    for k, player in enumerate(playerId):
        for i, updatedplayer in enumerate(updatedId):
            playerHash = {}
            if playerId[k] == updatedId[i]:
                playerHash['player_id'] = playerId[k]
                playerHash['player_name'] = playerName[k]
                playerHash['batting_strike_rate'] = battingStrikeRate[k]
                playerHash['batting_average'] = battingAverage[k]
                playerHash['balls_faced'] = ballsFaced[k]
                playerHash['km_batting_cluster_label'] = batting_km_labels_list[i]
                mainData.append(playerHash)

    return json.dumps(mainData)
import json
import numpy as np
from sklearn.cluster import KMeans
import warnings
from sklearn.preprocessing import normalize
from sklearn import metrics

# getBowlingCluster
# initialise the values
# filter the value based on the selected values
# cluster the values
# return the new cluster values

def getBowlingCluster(paramClusterCount,paramMinBowlerEconomy, paramMaxBowlerEconomy, paramMinBowlingAverage, paramMaxBowlingAverage):

    playerId = []
    playerName = []
    bowlingAverage = []
    bowlingEconomy = []
    bowlingStrikeRate = []
    ballsBowled = []
    totalDismissCount = []

    updatedBowlerId = []
    updatedBowlerEconomy = []
    updatedBowlingAverage = []
    updatedBowlingStrikeRate = []

    bowlingMainData = []

    cluster_count = paramClusterCount
    minBowlerEconomy = paramMinBowlerEconomy
    maxBowlerEconomy = paramMaxBowlerEconomy
    minBowlingAverage = paramMinBowlingAverage
    maxBowlingAverage = paramMaxBowlingAverage

    with open('./ClusterData/playerJsonData.json', 'r') as playerJson:
        jsonData = json.load(playerJson)
        for row in jsonData:
            playerId.append(row['player_id'])
            playerName.append(row['player_name'])
            bowlingAverage.append(row['bowling_average'])
            bowlingEconomy.append(row['bowling_economy'])
            bowlingStrikeRate.append(row['bowling_strike_rate'])
            ballsBowled.append(row['balls_bowled'])
            totalDismissCount.append(row['total_dismissal'])

    averageBallBowled = float("%.2f" % (sum(ballsBowled) / (len(ballsBowled) * 9)))

    for i, indexaverage in enumerate(playerId):

        if bowlingEconomy[i] >= minBowlerEconomy and bowlingEconomy[i] <= maxBowlerEconomy:
            if bowlingAverage[i] >= minBowlingAverage and bowlingAverage[i] <= maxBowlingAverage:
                if ballsBowled[i] >= averageBallBowled:
                    if bowlingAverage[i] != 0 and bowlingStrikeRate[i] != 0:
                        updatedBowlerId.append(playerId[i])
                        updatedBowlerEconomy.append(bowlingEconomy[i])
                        updatedBowlingAverage.append(bowlingAverage[i])
                        updatedBowlingStrikeRate.append(bowlingStrikeRate[i])

    bowlingCombinedData = np.vstack((updatedBowlerEconomy, updatedBowlingAverage, updatedBowlingStrikeRate)).T

    bowlingNormalizedData = normalize(bowlingCombinedData, axis=1, norm='l2')

    try:
        bowlingKmeans = KMeans(n_clusters=cluster_count, random_state=0).fit(bowlingNormalizedData)

    except ValueError:
        print("ValueError encountered in bowling cluster")

    bowling_km_labels = bowlingKmeans.labels_

    print("Bowling Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(bowlingNormalizedData, bowlingKmeans.labels_, sample_size=1000))

    warnings.filterwarnings('ignore',
                            '.*Graph is not fully connected, spectral embedding.*',
                            UserWarning,
                            )

    bowling_km_labels_list = bowling_km_labels.tolist()

    for k, player in enumerate(playerId):
        for j, bowlingUpdatedplayer in enumerate(updatedBowlerId):
            bowlingPlayerHash = {}
            if playerId[k] == updatedBowlerId[j]:
                bowlingPlayerHash['player_id'] = playerId[k]
                bowlingPlayerHash['player_name'] = playerName[k]
                bowlingPlayerHash['bowling_average'] = bowlingAverage[k]
                bowlingPlayerHash['bowling_economy'] = bowlingEconomy[k]
                bowlingPlayerHash['bowling_strike_rate'] = bowlingStrikeRate[k]
                bowlingPlayerHash['balls_bowled'] = ballsBowled[k]
                bowlingPlayerHash['km_bowling_cluster_label'] = bowling_km_labels_list[j]
                bowlingMainData.append(bowlingPlayerHash)

    return json.dumps(bowlingMainData)

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:49:59 2017

@author: Yuvaraj Subramanian
"""

import json
import numpy as np
from sklearn.cluster import KMeans
import warnings
from sklearn.preprocessing import normalize
from sklearn import metrics

def Clustering(paramClusterCount,paramMinBattingAverage,paramMaxBattingAverage,paramMinStrikeRate,paramMaxStrikeRate,paramMinBowlerEconomy,paramMaxBowlerEconomy,paramMinBowlingAverage,paramMaxBowlingAverage):

    playerId = []
    playerName = []
    battingStrikeRate = []
    battingAverage = []
    ballsFaced = []
    bowlingAverage = []
    bowlingEconomy = []
    bowlingStrikeRate = []
    ballsBowled = []
    totalDismissCount = []

    updatedId = []
    updatedStrikeRate = []
    updatedBattingAverage = []
    updatedBowlerId = []
    updatedBowlerEconomy = []
    updatedBowlingAverage = []
    updatedBowlingStrikeRate = []

    mainData = []
    bowlingMainData = []

    averageBallFaced = 30

    cluster_count=paramClusterCount
    minBattingAverage=paramMinBattingAverage
    maxBattingAverage=paramMaxBattingAverage
    minStrikeRate=paramMinStrikeRate
    maxStrikeRate=paramMaxStrikeRate
    minBowlerEconomy=paramMinBowlerEconomy
    maxBowlerEconomy=paramMaxBowlerEconomy
    minBowlingAverage=paramMinBowlingAverage
    maxBowlingAverage=paramMaxBowlingAverage

    with open('./ClusterData/playerJsonData.json', 'r') as playerJson:
        jsonData = json.load(playerJson)
        for row in jsonData:
            playerId.append(row['player_id'])
            playerName.append(row['player_name'])
            battingStrikeRate.append(row['batting_strike_rate'])
            battingAverage.append(row['batting_average'])
            ballsFaced.append(row['balls_faced'])
            bowlingAverage.append(row['bowling_average'])
            bowlingEconomy.append(row['bowling_economy'])
            bowlingStrikeRate.append(row['bowling_strike_rate'])
            ballsBowled.append(row['balls_bowled'])
            totalDismissCount.append(row['total_dismissal'])
                
    averageBallBowled=float ("%.2f" % (sum(ballsBowled)/(len(ballsBowled)*9)))
    
#    ##Below min,max values are added for testing 
#    
#    maxBattingAverage=max(battingAverage)
#    minBattingAverage=min(battingAverage)
#    maxStrikeRate = max(battingStrikeRate)
#    minStrikeRate = min(battingStrikeRate)
#    minBowlerEconomy=min(bowlingEconomy)
#    maxBowlerEconomy=max(bowlingEconomy)
#    minBowlingAverage=min(bowlingAverage)
#    maxBowlingAverage=max(bowlingAverage)
          
    for i,indexaverage in enumerate(playerId):
        
        if battingAverage[i] >= minBattingAverage and battingAverage[i] <= maxBattingAverage:
            if battingStrikeRate[i] >= minStrikeRate and battingStrikeRate[i] <= maxStrikeRate:
                if ballsFaced[i] >= 30:
                    if battingStrikeRate[i] != 0 and battingAverage[i] != 0:
                        if totalDismissCount[i] > 5:
                            updatedId.append(playerId[i])
                            updatedStrikeRate.append(battingStrikeRate[i])
                            updatedBattingAverage.append(battingAverage[i])
    
        if bowlingEconomy[i] >= minBowlerEconomy and bowlingEconomy[i] <= maxBowlerEconomy:
            if bowlingAverage[i] >= minBowlingAverage and bowlingAverage[i] <= maxBowlingAverage:
                if ballsBowled[i] >= averageBallBowled:
                    if bowlingAverage[i] != 0 and bowlingStrikeRate[i] != 0:
    #                    if bowlingEconomy[i] < 10:
    #                        if bowlingAverage[i] < 40:
                        updatedBowlerId.append(playerId[i])
                        updatedBowlerEconomy.append(bowlingEconomy[i])
                        updatedBowlingAverage.append(bowlingAverage[i])       
                        updatedBowlingStrikeRate.append(bowlingStrikeRate[i])
            
    combinedData = np.vstack((updatedBattingAverage,updatedStrikeRate)).T
    bowlingCombinedData = np.vstack((updatedBowlerEconomy, updatedBowlingAverage, updatedBowlingStrikeRate)).T
    
    battingNormalizedData = normalize(combinedData, axis=1, norm='l2')
    bowlingNormalizedData = normalize(bowlingCombinedData, axis=1, norm='l2')
    
    try:
        kmeanscluster = KMeans(n_clusters=cluster_count,random_state=0).fit(battingNormalizedData)
    
    except ValueError:
        print("ValueError encountered in batting cluster")
    
    km_labels = kmeanscluster.labels_
    
    try:
        bowlingKmeans = KMeans(n_clusters=cluster_count,random_state=0).fit(bowlingNormalizedData)
    
    except ValueError:
        print("ValueError encountered in bowling cluster")
    
    print("Batting Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(battingNormalizedData, kmeanscluster.labels_, sample_size=1000))
    
    
    bowling_km_labels = bowlingKmeans.labels_
    
    print("Bowling Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(bowlingNormalizedData, bowlingKmeans.labels_, sample_size=1000))
    
    warnings.filterwarnings('ignore', 
                            '.*Graph is not fully connected, spectral embedding.*', 
                            UserWarning,
                            )
    
    batting_km_labels_list = km_labels.tolist()
    bowling_km_labels_list = bowling_km_labels.tolist()
        
    for k,player in enumerate(playerId):
        for i,updatedplayer in enumerate(updatedId):
            playerHash = {}
            if playerId[k] == updatedId[i]:
    #            print (playerId[k], updatedId[i])
                playerHash['player_id'] = playerId[k]
                playerHash['player_name'] = playerName[k]
                playerHash['batting_strike_rate'] = battingStrikeRate[k]
                playerHash['batting_average'] = battingAverage[k]
                playerHash['balls_faced'] = ballsFaced[k]
                playerHash['km_batting_cluster_label'] = batting_km_labels_list[i]
                mainData.append(playerHash)
    
        
        for j,bowlingUpdatedplayer in enumerate(updatedBowlerId):
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
        
    return json.dumps(mainData),json.dumps(bowlingMainData)
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 00:25:28 2017

@author: Yuvaraj Subramanian
"""
import csv
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
import numpy as np
import json
import warnings

from sklearn import metrics

player_id = []
player_name = []
umpire = []

matchPlayedPId = []

Match_Id = []
StrikerID = []
Batsman_Scored = []
Extra_Type = []
playerDissimalId = []
bowlerId = []
extraRuns = []
dissimalType = []

strikeRate = []
battingAverage = []

bowlerEconomy = []
bowlingAverage = []
bowlingStrikeRate = []

ballsBowled = []
ballsFaced = []

totalFour = []
totalSix = []
averageFour = []
averageSix = []

Total_Score = []

a = []

cluster_count=4
#minBattingAverage=35
#maxBattingAverage=45
#minStrikeRate=50
#maxStrikeRate=150
#
#minBowlerEconomy=5
#maxBowlerEconomy=70
#minBowlingAverage=5
#maxBowlingAverage=450


def ClusteringMethod():

    with open('./indian-premier-league-csv-dataset/Player.csv', 'r') as playerfile:
        playerFileReader =csv.DictReader(playerfile)
        for row in playerFileReader:
            if (row['Is_Umpire']=="0"):
                player_id.append(row['Player_Id'])
                player_name.append(row['Player_Name'])
    
    with open('./indian-premier-league-csv-dataset/Player_Match.csv', 'r') as playerMatchFile:
        playerMatchFileReader =csv.DictReader(playerMatchFile)
        for row in playerMatchFileReader:
            matchPlayedPId.append(row['Player_Id'])
    
    with open('./indian-premier-league-csv-dataset/Ball_by_Ball.csv') as ballbybaplayerfile:
        ballByBallReader = csv.DictReader(ballbybaplayerfile)
        for row in ballByBallReader:
            Match_Id.append(row['Match_Id'])
            StrikerID.append(row['Striker_Id'])
            Batsman_Scored.append(row['Batsman_Scored'])
            Extra_Type.append(row['Extra_Type'])
            playerDissimalId.append(row['Player_dissimal_Id'])
            bowlerId.append(row['Bowler_Id'])
            extraRuns.append(row['Extra_Runs'])
            dissimalType.append(row['Dissimal_Type'])
            
        for index,i in enumerate(player_id):
            totalScore = 0
            ballCount = 0
            matchCount = 0
            matchDismissedCount = 0
            
            bowlerRun = 0
            bowlerBallCount = 0
            
            wicketCount=0
            fourCount = 0 
            sixCount = 0
    
            for indexk, k in enumerate(matchPlayedPId):
                if player_id[index] == matchPlayedPId[indexk]:
                    matchCount=matchCount+1
    
            for indexj,j in enumerate(Batsman_Scored):
    
                if Batsman_Scored[indexj] == " ":
                    Batsman_Scored[indexj] = 0
                elif Batsman_Scored[indexj] != "Do_nothing": 
                    if player_id[index] == playerDissimalId[indexj]:
                        matchDismissedCount=matchDismissedCount+1
                    if player_id[index] == StrikerID[indexj]:
                        if (Extra_Type[indexj] == "wides"):
                            totalScore+=int(Batsman_Scored[indexj])
                        else:
                            totalScore+=int(Batsman_Scored[indexj])
                            ballCount=ballCount+1
                            
                        if Batsman_Scored[indexj] == "4":
                            fourCount+=1
                        elif Batsman_Scored[indexj] == "6":
                            sixCount = sixCount +1
                            
                    if player_id[index] == bowlerId[indexj]:
                        if Extra_Type[indexj] == "wides" or Extra_Type[indexj] == "noballs":
                            bowlerRun+=int(Batsman_Scored[indexj])+int(extraRuns[indexj])
    #                        bowlerBallCount=bowlerBallCount-1;
                        else:
                            bowlerRun+=int(Batsman_Scored[indexj])
                            bowlerBallCount=bowlerBallCount+1
                                                
                        if dissimalType[indexj] == "caught" or dissimalType[indexj] == "bowled" or dissimalType[indexj] == "lbw" or dissimalType[indexj] == "stumped" or dissimalType[indexj] == "caught and bowled" or dissimalType[indexj] == "hit wicket" :
                            wicketCount=wicketCount+1
                        
            matchNotOutCount = matchCount - matchDismissedCount
    
            if ballCount == 0:
                stRate="%.2f" % (0.00)
            else:
                stRate="%.2f" % ((totalScore / ballCount)*100)
    
            if totalScore == 0:
                battingAvg="%.2f" % (0.00)
            elif matchCount-matchNotOutCount == 0:
                battingAvg="%.2f" % (0.00)
            else:
                battingAvg="%.2f" % (totalScore/(matchCount-matchNotOutCount))
                
            Total_Score.append(float(totalScore))
            strikeRate.append(float(stRate))
            battingAverage.append(float(battingAvg))
            ballsFaced.append(int(ballCount))
            
            totalFour.append(int(fourCount))
            totalSix.append(int(sixCount))
            
    #        Calculating average fours by the player
            
            if fourCount > 0 and ballCount > 0:
                avgFour = "%.2f" % ((fourCount/ballCount)*100)
            else:
                avgFour = "%.2f" % (0.00)    
            averageFour.append(avgFour)
            
    #        Calculating average six by the player
                    
            if sixCount > 0 and ballCount > 0:
                avgSix = "%.2f" % ((sixCount/ballCount)*100)
            else:
                avgSix = "%.2f" % (0.00)    
            averageSix.append(avgSix)        
            
            if bowlerRun == 0:
                economy="%.2f" % (0.00)
            else:
                economy="%.2f" % (bowlerRun/(bowlerBallCount/6))
                
            if wicketCount == 0:
                bowaverage="%.2f" % (0.00)
                bowlingStrRate="%.2f" % (0.00)
            else:
                bowaverage ="%.2f" %  (bowlerRun/wicketCount)
                bowlingStrRate = "%.2f" %  (bowlerBallCount/wicketCount)
            
            bowlingStrikeRate.append(float(bowlingStrRate))
            bowlingAverage.append(float(bowaverage))
            ballsBowled.append(int(bowlerBallCount))
            bowlerEconomy.append(float(economy))
            
    #Calculating updated values
    
    updatedId = []
    updatedStrikeRate= []
    updatedBattingAverage=[]
    
    averageBallFaced=30
#    
#    if maxBattingAverage == None:
#        maxBattingAverage=max(battingAverage)
#        
#    elif minBattingAverage == None:
#        minBattingAverage=min(battingAverage)
#        
#    elif maxStrikeRate == None:
#        maxStrikeRate = max(strikeRate)
#        
#    elif minStrikeRate == None:
#        minStrikeRate = min(strikeRate)
        
    maxBattingAverage=max(battingAverage)
    minBattingAverage=min(battingAverage)
    maxStrikeRate = max(strikeRate)
    minStrikeRate = min(strikeRate)
    
    for i,indexaverage in enumerate(player_id):
        if battingAverage[i] >= minBattingAverage and battingAverage[i] <= maxBattingAverage:
            if strikeRate[i] >= minStrikeRate and strikeRate[i] <= maxStrikeRate:
                if ballsFaced[i] >= averageBallFaced:
                    if strikeRate[i] != 0.00 and battingAverage[i] != 0.00:
                        updatedId.append(player_id[i])
                        updatedStrikeRate.append(strikeRate[i])
                        updatedBattingAverage.append(battingAverage[i])
                        
    combinedData = np.vstack((updatedBattingAverage,updatedStrikeRate)).T
    
    #print(combinedData)
      
    #try:
    km = KMeans(n_clusters=cluster_count,random_state=0).fit(combinedData)
    specCluster=SpectralClustering(n_clusters=cluster_count, affinity="nearest_neighbors").fit(combinedData)
    
    #except ValueError:
    #    print("ValueError encountered")
    
    centroids = km.cluster_centers_
    km_labels = km.labels_
    
    # Metrics have been referred from http://scikit-learn.org/stable/auto_examples/text/document_clustering.html#sphx-glr-auto-examples-text-document-clustering-py
    
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(km_labels, km.labels_))
    print("Completeness: %0.3f" % metrics.completeness_score(km_labels, km.labels_))
    print("V-measure: %0.3f" % metrics.v_measure_score(km_labels, km.labels_))
    print("Adjusted Rand-Index: %.3f"
          % metrics.adjusted_rand_score(km_labels, km.labels_))
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(combinedData, km.labels_, metric='euclidean', sample_size=1000))
    
    # --- BOWLING --- #
    
    updatedBowlerId = []
    updatedBowlerEconomy= []
    updatedBowlingAverage=[]
    updatedBowlingStrikeRate=[]
    
    #Demo purpose
    
    minBowlerEconomy=min(bowlerEconomy)
    maxBowlerEconomy=max(bowlerEconomy)
    minBowlingAverage=min(bowlingAverage)
    maxBowlingAverage=max(bowlingAverage)
    
    averageBallBowled=float ("%.2f" % (sum(ballsBowled)/(len(ballsBowled)*9)))
    #print (averageBallBowled)
    
    for i,bowaverage in enumerate(player_id):
        if bowlerEconomy[i] >= minBowlerEconomy and bowlerEconomy[i] <= maxBowlerEconomy:
            if bowlingAverage[i] >= minBowlingAverage and strikeRate[i] <= maxBowlingAverage:
                if ballsBowled[i] >= averageBallBowled:
                    if bowlingAverage[i] != 0.00 and bowlingStrikeRate[i] != 0.00:
                        updatedBowlerId.append(player_id[i])
                        updatedBowlerEconomy.append(bowlerEconomy[i])
                        updatedBowlingAverage.append(bowlingAverage[i])       
                        updatedBowlingStrikeRate.append(bowlingStrikeRate[i])
    
    bowlingCombinedData = np.vstack((updatedBowlerEconomy, updatedBowlingAverage, updatedBowlingStrikeRate)).T
    
    affMatrix = specCluster.affinity_matrix_
    sc_labels = specCluster.labels_
    
    try:
        bowlingKmeans = KMeans(n_clusters=cluster_count).fit(bowlingCombinedData)
        bowlingSpecCluster=SpectralClustering(n_clusters=cluster_count, affinity="nearest_neighbors").fit(bowlingCombinedData)
    
    except ValueError:
        print("ValueError encountered")
        
    bowling_km_labels = bowlingKmeans.labels_
    bowling_sc_labels = bowlingSpecCluster.labels_
    
    warnings.filterwarnings('ignore', 
                            '.*Graph is not fully connected, spectral embedding.*', 
                            UserWarning,
                            )
        
    mainData = []
    bowlingMainData= []
    
    batting_km_labels_list=km_labels.tolist()
    batting_sc_labels_list=sc_labels.tolist()
    
    bowling_km_labels_list = bowling_km_labels.tolist()
    bowling_sc_labels_list = bowling_sc_labels.tolist()
    
    for i,player in enumerate(player_id):
        for j,updatedplayer in enumerate(updatedId):
            playerHash = {}
            if player_id[i] == updatedId[j]:
                playerHash['player_id'] = player_id[i]
                playerHash['player_name'] = player_name[i]
                playerHash['batting_strike_rate'] = strikeRate[i]
                playerHash['batting_average'] = battingAverage[i]
                playerHash['total_fours'] = totalFour[i]
                playerHash['average_fours_in_percentage'] = averageFour[i]
                playerHash['total_six'] = totalSix[i]
                playerHash['average_six_in_percentage'] = averageSix[i]
                playerHash['balls_faced'] = ballsFaced[i]
                playerHash['km_batting_cluster_label'] = batting_km_labels_list[j]
                playerHash['sc_batting_cluster_label'] = batting_sc_labels_list[j]
        
                mainData.append(playerHash)
        
        for j,bowlingUpdatedplayer in enumerate(updatedBowlerId):
            bowlingPlayerHash = {}
            if player_id[i] == updatedBowlerId[j]:
                bowlingPlayerHash['player_id'] = player_id[i]
                bowlingPlayerHash['player_name'] = player_name[i]
                bowlingPlayerHash['bowling_average'] = bowlingAverage[i]
                bowlingPlayerHash['bowling_economy'] = bowlerEconomy[i]
                bowlingPlayerHash['bowling_strike_rate'] = bowlingStrikeRate[i]
                bowlingPlayerHash['balls_bowled'] = ballsBowled[i]
                bowlingPlayerHash['km_bowling_cluster_label'] = bowling_km_labels_list[j]
                bowlingPlayerHash['sc_bowling_cluster_label'] = bowling_sc_labels_list[j]  
            
                bowlingMainData.append(bowlingPlayerHash)
    
    with open('./ClusterData/jsonData.json', 'w') as mainDataJSON:
        json.dump(mainData,mainDataJSON)
        
    with open('./ClusterData/bowlingJsonData.json', 'w') as bowlingDataJSON:
        json.dump(bowlingMainData,bowlingDataJSON)
    
#    return json.dumps(mainData),json.dumps(bowlingMainData)
        
ClusteringMethod()
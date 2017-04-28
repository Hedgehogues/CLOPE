# -*- coding: utf-8 -*-

import copy
import CLOPE
import pickle


with open('data/users.pickle', 'rb') as f:
    dataGroups = pickle.load(f)

dataNew = {}
index = 0
countElements = 50000
for item in dataGroups:
    if countElements > 0 and index > countElements:
        break
    dataNew[item] = dataGroups[item]
    index += 1
dataGroups = copy.deepcopy(dataNew)
repulsion = 1.0015
noiseLimit = -1
isSaveHistory = False
iter = 10000
countTransfer = 1000000
stopLimit = 300

clope = CLOPE.CData()
clope.Init(dataGroups, iter, repulsion, isSaveHistory, noiseLimit)
print("Инициализация завершена. Число кластеров: ", len(clope.Clusters))
while countTransfer > stopLimit:
    countTransfer = clope.NextStep(dataGroups, iter, repulsion, isSaveHistory, noiseLimit)
    print("Число перемещений между кластерами", countTransfer, ". Число кластеров: ", len(clope.Clusters))

with open('data/CLOPE_users' + '.r=' + str(repulsion) + '.stopLimit=' + str(stopLimit) + '.pickle', 'wb') as f:
    pickle.dump(clope, f)
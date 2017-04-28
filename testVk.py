# -*- coding: utf-8 -*-

import CLOPE
import pickle


dataGroups = []

with open('data/CLOPE_users.r=1.009.stopLimit=300.pickle', 'rb') as f:
    clopeLoad = pickle.load(f)

with open('data/users.pickle', 'rb') as f:
    dataGroups = pickle.load(f)

repulsion = 1.03
isSaveHistory = False
iter = 2000
countTransfer = 1000000
stopLimit = 300

clope = CLOPE.CData()
clope.Init(dataGroups, iter, repulsion, isSaveHistory)
print("Инициализация завершена")
while countTransfer > stopLimit:
    countTransfer = clope.NextStep(dataGroups, iter, repulsion, isSaveHistory)
    print("Число перемещений между кластерами", countTransfer)

with open('data/CLOPE_users' + '.r=' + str(repulsion) + '.stopLimit=' + str(stopLimit) + '.pickle', 'wb') as f:
    pickle.dump(clope, f)
# -*- coding: utf-8 -*-
import CLOPE
import json

# Прочитываем данные
with open('data/clope_features.json', 'r') as f:
    clients = json.load(f)

clope = CLOPE.CData()
# Начальные данные
iter = 1000
repulsion = 2
isSaveHist = True
noiseLimit = 0
max_count_clusters = 10
random_state = 41
# Инициализируем алгоритм
clope.Init(clients, iter, repulsion, isSaveHist, noiseLimit, max_count_clusters, random_state)
clope.PrintHistoryCount()
# Итерируемся
while clope.NextStep(clients, iter, repulsion, isSaveHist, noiseLimit, max_count_clusters, random_state) > 0:
    clope.PrintHistoryCount()

# Выводим распределение по кластерам съедобных и несъедобных грибов
answ = []
for item in range(0, len(clope.Clusters)):
    answ.append({'e': 0, 'p': 0})
for itemTransact in clope.Transaction:
    classter = clope.Transaction[itemTransact]
print(answ)
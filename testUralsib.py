# -*- coding: utf-8 -*-
import CLOPE
import json

# Прочитываем данные
with open('data/clope_features.json', 'r') as f:
    clients = json.load(f)

clope = CLOPE.Clope()
# Начальные данные
iter = 1000
repulsion = 2.3
isSaveHist = True
noiseLimit = 0
max_count_clusters = 40
random_state = 42
# Инициализируем алгоритм
clope.init(clients, iter, repulsion, isSaveHist, noiseLimit, max_count_clusters, random_state)
clope.print_history_count()
# Итерируемся
# while clope.NextStep(clients, iter, 2, isSaveHist, 5000, max_count_clusters, random_state) > 0:
#    clope.PrintHistoryCount()

# Выводим распределение по кластерам съедобных и несъедобных грибов
clusters = {}
for itemTransact in clope.transaction:
    cl_num = clope.transaction[itemTransact]
    if not cl_num in clusters:
        clusters[cl_num] = []
    clusters[cl_num].append(itemTransact)

with open('data/clusters.json', 'w') as f:
    json.dump(clusters, f)
clope.init(clients, iter, 10, isSaveHist, noiseLimit, max_count_clusters, random_state)
clope.print_history_count()
# Итерируемся
while clope.next_step(clients, iter, 2, isSaveHist, 5000, max_count_clusters, random_state) > 0:
    clope.print_history_count()

# Выводим распределение по кластерам съедобных и несъедобных грибов
answ = []
for item in range(0, len(clope.clusters)):
    answ.append({'e': 0, 'p': 0})
for itemTransact in clope.transaction:
    classter = clope.transaction[itemTransact]
print(answ)

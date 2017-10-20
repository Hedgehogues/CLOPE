# -*- coding: utf-8 -*-
import CLOPE
import json

# Прочитываем данные
with open('data/clope_features.json', 'r') as f:
    clients = json.load(f)

clope = CLOPE.Clope()
# Начальные данные
iter = 1000
repulsion = 10
isSaveHist = True
noiseLimit = 0
max_count_clusters = 10
random_state = 41
# Инициализируем алгоритм
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
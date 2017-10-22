# -*- coding: utf-8 -*-

import CLOPE
import pickle


# Инициализация параметров алгоритма
repulsion = 1.0015
noiseLimit = 10
isSaveHistory = False
iter = 10000
countTransfer = 1000000
stopLimit = 300

# Загрузка данных о пользователях
with open('data/users.pickle', 'rb') as f:
    dataGroups = pickle.load(f)

# Загрузка существующей кластеризации
with open('data/CLOPE_users' + '.r=' + str(repulsion) + '.stopLimit=' + str(stopLimit) + '.pickle', 'rb') as f:
    clope = pickle.load(f)

noiseTransaction = {}
for item in clope.Transaction:
    if clope.Transaction[item] in clope.NoiseClusters:
        noiseTransaction[item] = dataGroups[item]

# Выполнение алгоритма для шумовых кластеров
stopLimit = 0
clopeNoise = CLOPE.CLOPE()
clopeNoise.init_clusters(noiseTransaction, iter, repulsion, isSaveHistory, noiseLimit)
print("Инициализация завершена. Число кластеров: ", len(clopeNoise.clusters), ". Число шумовых кластеров при базовой кластеризации: ", len(clope.NoiseClusters))
while countTransfer > stopLimit:
    countTransfer = clopeNoise.next_step(noiseTransaction, iter, repulsion, isSaveHistory, noiseLimit)
    print("Число перемещений между кластерами", countTransfer, ". Число кластеров: ", len(clopeNoise.clusters), ". Число шумовых кластеров при базовой кластеризации: ", len(clope.NoiseClusters))

with open('data/CLOPE_users_noise' + '.r=' + str(repulsion) + '.stopLimit=' + str(stopLimit) + '.pickle', 'wb') as f:
    pickle.dump(clope, f)
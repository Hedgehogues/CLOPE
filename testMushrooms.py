# -*- coding: utf-8 -*-
import CLOPE
import numpy
import pandas as pd


def get_count_clusters(data, clope):
    # Выводим распределение по кластерам съедобных и несъедобных грибов
    answ = []
    for item in range(0, clope.max_cluster_number):
        answ.append({'e': 0, 'p': 0})
    for itemTransact in clope.transaction:
        cluster = clope.transaction[itemTransact]
        if data[itemTransact][0] == 'e':
            answ[cluster]['e'] += 1
        else:
            answ[cluster]['p'] += 1

    return pd.DataFrame(answ)


# Прочитываем данные
f = open('data/agaricus-lepiota.data.txt', 'r')
# Разделяем данные
mushroomsStart = [item.replace('\n', '').split(',') for item in f.readlines()]
seed = 40
numpy.random.seed(seed)
numpy.random.shuffle(mushroomsStart)
mushrooms = {}
for exampleIndex in range(0, len(mushroomsStart)):
    for index in range(0, len(mushroomsStart[exampleIndex])):
        # Первый столбец -- признак (съедобные (e) или нет(p)). Данный столбец является целым классом. По этому столбцу
        # проверяется качество тестирования
        if index != 0:
            if mushroomsStart[exampleIndex][index] != '?':
                mushrooms[exampleIndex][index - 1] = mushroomsStart[exampleIndex][index] + str(index)
            else:
                print('miss object')
        else:
            mushrooms[exampleIndex] = [''] * 22


clope = CLOPE.CLOPE(print_step=1000, is_save_history=True, random_seed=seed)
# Начальные данные
repulsion = 3
noiseLimit = 0
# Инициализируем алгоритм
clope.init_clusters(mushrooms, repulsion, noiseLimit)
df = get_count_clusters(clope)
clope.print_history_count(repulsion, seed)
# Итерируемся
while clope.next_step(mushrooms, repulsion, noiseLimit) > 0:
    clope.print_history_count(repulsion, seed)

get_count_clusters(mushroomsStart, clope)
# -*- coding: utf-8 -*-
import CLOPE
import numpy


# Прочитываем данные
f = open ('data/agaricus-lepiota.data.txt', 'r')
# Разделяем данные
mushroomsStart = [item.replace('\n', '').split(',') for item in f.readlines()]
numpy.random.seed(42)
numpy.random.shuffle(mushroomsStart)
mushrooms = {}
for exampleIndex in range(0, len(mushroomsStart)):
   for index in range(0, len(mushroomsStart[exampleIndex])):
       # Первый столбец -- признак (съедобные (e) или нет(p)). Данный столбец является целым классом. По этому столбцу
       # проверяется качество тестирования
       if index != 0:
           mushrooms[exampleIndex][index - 1] = mushroomsStart[exampleIndex][index] + str(index)
       else:
           mushrooms[exampleIndex] = [''] * 22

clope = CLOPE.Clope(print_step=1000, is_save_history=True)
# Начальные данные
iter = 1000
repulsion = 3
isSaveHist = True
noiseLimit = 0
# Инициализируем алгоритм
clope.init(mushrooms, repulsion, noiseLimit)
clope.print_history_count()
# Итерируемся
while clope.next_step(mushrooms, repulsion, noiseLimit) > 0:
    clope.print_history_count()

# Выводим распределение по кластерам съедобных и несъедобных грибов
answ = []
for item in range(0, clope.max_cluster_number):
    answ.append({'e': 0, 'p': 0})
for itemTransact in clope.transaction:
    cluster = clope.transaction[itemTransact]
    if mushroomsStart[itemTransact][0] == 'e':
        answ[cluster]['e'] += 1
    else:
        answ[cluster]['p'] += 1
print(answ)
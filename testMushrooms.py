# -*- coding: utf-8 -*-

import CLOPE



# Прочитываем данные
f = open ('data/agaricus-lepiota.data.txt', 'r')
# Разделяем данные
mushroomsStart = [item.replace('\n', '').split(',') for item in f.readlines()]
mushrooms = {}
for exampleIndex in range(0, len(mushroomsStart)):
   for index in range(0, len(mushroomsStart[exampleIndex])):
       # Первый столбец -- признак (съедобные (e) или нет(p)). Данный столбец является целым классом. По этому столбцу
       # проверяется качество тестирования
       if index != 0:
           mushrooms[exampleIndex][index - 1] = mushroomsStart[exampleIndex][index] + str(index)
       else:
           mushrooms[exampleIndex] = [''] * 22

clope = CLOPE.CData()
# Начальные данные
iter = 1000
repulsion = 2.7
isSaveHist = True
noiseLimit = 0
# Инициализируем алгоритм
clope.Init(mushrooms, iter, repulsion, isSaveHist, noiseLimit)
clope.PrintHistoryCount()
# Итерируемся
while clope.NextStep(mushrooms, iter, repulsion, isSaveHist, noiseLimit) > 0:
    clope.PrintHistoryCount()

# Выводим распределение по кластерам съедобных и несъедобных грибов
answ = []
for item in range(0, len(clope.Clasters)):
    answ.append({'e': 0, 'p': 0})
for itemTransact in clope.Transaction:
    classter = clope.Transaction[itemTransact]
    if mushroomsStart[itemTransact][0] == 'e':
        answ[classter]['e'] += 1
    else:
        answ[classter]['p'] += 1
print(answ)
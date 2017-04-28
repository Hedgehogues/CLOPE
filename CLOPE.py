# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# Класс, описывающий кластер
class CCluster:
    # Гистограмма
    Histogram = {}
    # Площадь гистограммы
    Area = 0.0
    # Высота гистограммы (в смысле H = S / W). Данная величина нигде в явном виде не вычисляется. Хранится в классе для
    # полноты описания класса и не более того.
    Height = 0.0
    # Ширина гистограммы (в смысле числа элементов)
    Width = 0.0
    # Градиент (в смысле G = H / W). Данная величина нигде в явном виде не вычисляется. Хранится в классе для полноты
    # описания класса и не более того.
    Gradient = 0.0
    # Число транзакций
    CountTransactions = 0
    # История количества транзакций в кластерах
    HistoryCountTransact = np.array([])

    def __init__(self):
        self.Area = 0.0
        self.Height = 0.0
        self.Width = 0.0
        self.Gradient = 0.0
        self.CountTransactions = 0.0
        self.Histogram = {}

    # Добавить транзакцию в кластер. Перебираем все элементы гистограммы, достраиваем гистограмму
    # Input parametres:
    # transaction -- слайс с объектами (транзакция)
    def AddTransaction(self, transaction):
        # Поочерёдно перебираем все элементы гистограммы и добавляем в соответствующий столбец гистограммы. Если
        # рассматриваемого элемента нет, то добавим новый столбец в гистограмму
        for item in transaction:
            if not (item in self.Histogram):
                self.Histogram[item] = 1
            else:
                self.Histogram[item] += 1
        # Вчисляем суммарную площадь гистограммы в смысле CLOPE (количество транзакций)
        self.Area += float(len(transaction))
        # Вычисляем ширину гистограммы (количество различных объектов)
        self.Width = float(len(self.Histogram))
        # Подсчитываем число транзакций в кластере
        self.CountTransactions += 1

    # Удалить транзакцию из кластера. Перебираем все элементы гистограммы, убираем все элементы транзакции из
    # гистограммы
    # Input parametres:
    # transaction -- слайс с объектами (транзакция)
    # NOTE: внутри класса не происходит слежение за тем, какие транзакции добавляются, какие удаляются, поэтому, если в
    # процессе модификации будет исключена транзакция, которая не была добавлена в соответствующий кластер, алгоритм
    # выдаст неверный результат
    def RemoveTransaction(self, transaction):
        for item in transaction:
            if self.Histogram[item] == 0:
                del self.Histogram[item]
        self.Area -= float(len(transaction))
        self.Width = float(len(self.Histogram))
        self.CountTransactions -= 1
        return self.Gradient

# Класс, описывающий работу с данными
class CData:
    # Максимальный номер кластера
    MaxClusterNumber = 0
    # Список кластеров
    Clusters = {} # CCluster
    # Количество добавленных транзакций
    CountTransactions = 0
    # Словарь. Ключи -- номер транзакции. Значение -- номер кластера
    Transaction = {}
    # Номер итерации
    Iteration = 0
    # Номера шумовых кластеров
    # Данный объект необходим для того, чтобы не брать во внимание те объкты, которые были отнесены к шумовым
    NoiseClusters = {}

    def __init__(self):
        self.Clusters = {}
        self.NoiseClusters = {}
        self.CountTransactions = 0
        self.Iteration = 0
        self.Transaction = {}
        self.MaxClusterNumber = 0

    # Рассчитывается изменение Goal, которое получит целевая функция при добавлении транзакции к кластеру clusterNumber.
    # Кластер, доставляющий максимальное значение функции, будет искомым кластером (в который следует добавить транзакцию)
    # Input parametres:
    # transaction -- транзакция (список объектов)
    # clusterNumber -- номер кластера, приращение для которого рассчитывается
    # r -- отталкивание в смысле CLOPE
    # Returned value:
    # Возвращает значение изменения целевой функции при добавлении transaction к кластеру clusterNumber
    def DeltaAddTransaction(self, transaction, clusterNumber, r):
        area = self.Clusters[clusterNumber].Area + len(transaction)
        width = self.Clusters[clusterNumber].Width
        for item in transaction:
            if not (item in self.Clusters[clusterNumber].Histogram):
                width += 1
        if width != 0:
            newDeltaValue = area * (self.Clusters[clusterNumber].CountTransactions + 1) / (width ** r)
        else:
            newDeltaValue = 0
        if self.Clusters[clusterNumber].Width != 0:
            oldDeltaValue = self.Clusters[clusterNumber].Area * self.Clusters[clusterNumber].CountTransactions / (
            self.Clusters[clusterNumber].Width ** r)
        else:
            oldDeltaValue = 0
        return newDeltaValue - oldDeltaValue

    # Функция удаления шума. Все кластеры, размер которых больше limit остаются
    # Input parametres:
    # limit -- уровень шума кластеров
    def NoiseReduction(self, limit):
        # Удаляем все пустые кластеры
        newClusters = {}
        for item in self.Clusters:
            if self.Clusters[item].CountTransactions > limit:
                newClusters[item] = self.Clusters[item]
            else:
                self.NoiseClusters[item] = True
        self.Clusters = newClusters

    # Вычисление целевой функции для всех уже сформированных кластеров
    # Используется при модификации кластеров, либо их инициализации
    # Input parametres:
    # r -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    # Returned value:
    # Возвращает значение целевой функции
    def GetGoalFunction(self, r):
        measure = 0.0
        # Перебираем все кластеры и для каждого рассчитываем его вес. Все веса суммируются в общую метрику
        for item in self.Clusters:
            if item.Width == 0:
                # print "test"
                pass
            else:
                # Попытка подобрать иную метрику
                # measure += (r ** 2 * math.log(item.Area ** (1 / r) / item.Width) ** 2) * item.CountTransactions / self.CountTransactions
                measure += item.Area / (item.Width ** r) * item.CountTransactions / self.CountTransactions
        return measure

    # Модификация транзакции
    # Пытаемся перебросить транзакцию (transaction) с номером id в другой класс
    # Input parametres:
    # transaction -- транзакция (слайс с объектами)
    # id -- номер транзакции
    # repulsion -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    # isSaveHistory -- флаг, выставляемый при необходимости записи истории количества транзакций
    # Returned value:
    # Возвращает значение, отвечающие наличию изменения кластера или его отсутствию
    def ModifyTransactions(self, transaction, id, repulsion = 2, isSaveHistory = True):
        # Смотрим, где данная транзакция лежит сейчас
        clusterNumber = self.Transaction[id]
        # Если транзакция относится к шумовому кластеру, то не пытаемся её поменять
        if clusterNumber in self.NoiseClusters:
            return 0
        # Извлекаем транзакцию из текущего кластера
        self.Clusters[clusterNumber].RemoveTransaction(transaction)
        # Рассматриваем транзакцию как вновь пришедшую и добавляем в тот кластер, где значение целевой функции доставит
        # максимум
        return int(self.AddNewTransaction(transaction, id, repulsion, isSaveHistory) != clusterNumber)

    # Добавление новой транзакции
    # Пытаемся перераспределить транзакцию (transaction) с номером id в другой класс так, чтобы целевая функция приняла
    # максимальное значение
    # Input parametres:
    # transaction -- транзакция (слайс с объектами)
    # id -- номер транзакции
    # repulsion -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    # isSaveHistory -- флаг, выставляемый при необходимости записи истории количества транзакций
    # Returned parameter:
    # Возвращается номер кластера, в который была добавлена текущая транзакция
    def AddNewTransaction(self, transaction, id, repulsion = 2, isSaveHistory = True):
        r = repulsion
        maxValue = -1
        maxValueIndex = -1
        self.CountTransactions += 1
        # Ищем кластер, на котором будет достигнуто максимальное значение изменения целевой функции
        for clusterNumber in self.Clusters:
            delta = self.DeltaAddTransaction(transaction, clusterNumber, r)
            if delta > 0 and delta > maxValue:
                maxValueIndex = clusterNumber
                maxValue = delta
        # Добавляем транзакцию в новый кластер и смотрим на результат
        self.Clusters[self.MaxClusterNumber] = CCluster()
        valueGoalFunction = self.DeltaAddTransaction(transaction, self.MaxClusterNumber, r)
        if valueGoalFunction > maxValue:
            maxValueIndex = self.MaxClusterNumber
        self.MaxClusterNumber += 1

        # Запоминаем, в каком кластере лежит текущая транзакция
        self.Transaction[id] = maxValueIndex
        if maxValueIndex != len(self.Clusters) - 1:
            self.MaxClusterNumber -= 1
            del self.Clusters[self.MaxClusterNumber]
        else:
            if isSaveHistory:
                self.Clusters[-1].HistoryCountTransact = np.array([0] * len(self.Clusters[0].HistoryCountTransact))

        # Добавляем транзакцию в необходимый кластер
        self.Clusters[maxValueIndex].AddTransaction(transaction)

        if isSaveHistory:
            for itemCluster in self.Clusters:
                itemCluster.HistoryCountTransact = np.append(itemCluster.HistoryCountTransact, itemCluster.CountTransactions)

        return maxValueIndex

    # Адаптивное вычисление порога шума. Порог вычистывается относительно медианы размеров кластеров (в числе
    # транзакций). Берётся 3/4 медианы
    def GetNoiseLimit(self):
        sizeClusters = []
        for item in self.Clusters:
            sizeClusters.append(self.Clusters[item].CountTransactions)
        sorted(sizeClusters)
        medianElement = int(3 * len(sizeClusters) / 4) + 1
        if len(sizeClusters) < 5:
            limit = 10
        else:
            limit = sizeClusters[medianElement]
        return limit

    # Инициализация алгоритма
    # Input parametres:
    # data -- слайс с транзакциями
    # isPrint -- нужно ли печатать информацию о ходе выполнения (0 -- не нужно, если > 0 -- печатаем каждый isPrint раз)
    # repulsion -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    # isSaveHistory -- флаг, выставляемый при необходимости записи истории количества транзакций
    # isNoiseReduction -- подавление шума (порог соответствует числу элементов в кластере, при котором он уничтожается).
    #                     Если isNoiseReduction == -1, то порог выбирается адаптивно (всё то, что больше медианы
    #                     остаётся)
    def Init(self, data, isPrint, repulsion = 2, isSaveHistory = True, isNoiseReduction = -1):
        index = 0
        for item in data:
            self.AddNewTransaction(data[item], item, repulsion, isSaveHistory)
            index += 1
            if isPrint > 0 and index % isPrint == 0:
                print("Итерация: ", self.Iteration, ". Номер шага", index, ". Число кластеров: ", len(self.Clusters))

        if isNoiseReduction < 0:
            isNoiseReduction = self.GetNoiseLimit()
        # Удаляем все шумовые кластеры (после инициализации не бывает пустых классов, поэтому знак строго больше)
        if isNoiseReduction > 0:
            self.NoiseReduction(isNoiseReduction)

        print(isNoiseReduction)

        self.Iteration = 1

    # Выполнение алгоритма. Выполнение следующего шага
    # Input parametres:
    # data -- слайс с транзакциями
    # isPrint -- нужно ли печатать информацию о ходе выполнения (0 -- не нужно, если > 0 -- печатаем каждый isPrint раз)
    # repulsion -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    # isSaveHistory -- флаг, выставляемый при необходимости записи истории количества транзакций
    # isNoiseReduction -- подавление шума (порог соответствует числу элементов в кластере, при котором он уничтожается).
    #                     Если isNoiseReduction == -1, то порог выбирается адаптивно (всё то, что больше медианы
    #                     остаётся)
    # Returned parameter:
    # Возвращается число операций по перенесению транзакции из кластера в кластер
    def NextStep(self, data, isPrint, repulsion = 2, isSaveHistory = True, isNoiseReduction = -1):
        index = 0
        eps = 0
        for item in data:
            eps += self.ModifyTransactions(data[item], item, repulsion, isSaveHistory)
            index += 1
            if isPrint > 0 and index % isPrint == 0:
                print("Итерация: ", self.Iteration, ". Номер шага", index, ". Число кластеров: ", len(self.Clusters))
        self.Iteration += 1

        # Удаляем все пустые (или шумовые, если isNoiseReduction > 0) кластеры
        if isNoiseReduction < 0:
            isNoiseReduction = self.GetNoiseLimit()
        self.NoiseReduction(isNoiseReduction)
        print(isNoiseReduction)
        return eps

    # Рисуем график, демонстрирующий количество транзакций в различных классах
    def PrintHistoryCount(self):
        for itemCluster in self.Clusters:
            x = np.array(range(0, len(self.Transaction) * self.Iteration))
            if len(itemCluster.HistoryCountTransact) != 0:
                y = itemCluster.HistoryCountTransact
            else:
                y = [0] * len(self.Transaction) * self.Iteration
            plt.plot(x, y)
        plt.xlabel(u"Iteration number")
        plt.ylabel(u"Count transactions")
        plt.title(u"Charts for changing the number of transactions in clusters")
        plt.show()
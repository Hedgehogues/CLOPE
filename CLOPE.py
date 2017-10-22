# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


class Cluster:

    def __init__(self, history_count):
        # История количества транзакций в кластерах
        self.history_count_transact = [0] * history_count
        # Площадь гистограммы
        self.area = 0.0
        # Высота гистограммы (в смысле H = S / W). Данная величина нигде в явном виде не вычисляется.
        # Хранится в классе для полноты описания класса и не более того.
        self.height = 0.0
        # Ширина гистограммы (в смысле числа элементов)
        self.width = 0.0
        # Градиент (в смысле G = H / W). Данная величина нигде в явном виде не вычисляется. Хранится в классе
        # для полноты описания класса и не более того.
        self.gradient = 0.0
        # Число транзакций
        self.count_transactions = 0
        # Гистограмма
        self.histogram = {}

    '''
    Добавить транзакцию в кластер. Перебираем все элементы гистограммы, достраиваем гистограмму
    Input parametres:
    transaction -- слайс с объектами (транзакция)
    '''
    def add_transaction(self, transaction):
        # Поочерёдно перебираем все элементы гистограммы и добавляем в соответствующий столбец гистограммы. Если
        # рассматриваемого элемента нет, то добавим новый столбец в гистограмму
        for item in transaction:
            if not (item in self.histogram):
                self.histogram[item] = 1
            else:
                self.histogram[item] += 1
        # Вчисляем суммарную площадь гистограммы в смысле CLOPE (количество транзакций)
        self.area += float(len(transaction))
        # Вычисляем ширину гистограммы (количество различных объектов)
        self.width = float(len(self.histogram))
        # Подсчитываем число транзакций в кластере
        self.count_transactions += 1

    '''
    Удалить транзакцию из кластера. Перебираем все элементы гистограммы, убираем все элементы транзакции из
    гистограммы
    
    Input parametres:
    transaction -- слайс с объектами (транзакция)
    Returned values:
    величина градиента G(transaction)
    
    Внутри класса не происходит слежение за тем, какие транзакции добавляются, какие удаляются, поэтому, если в
    процессе модификации будет исключена транзакция, которая не была добавлена в соответствующий кластер, алгоритм
    выдаст неверный результат
    '''
    def remove_transaction(self, transaction):
        for item in transaction:
            if self.histogram[item] == 0:
                del self.histogram[item]
        self.area -= float(len(transaction))
        self.width = float(len(self.histogram))
        self.count_transactions -= 1
        return self.gradient


class CLOPE:

    def __init__(self, is_save_history=True, print_step=1000, random_seed=None):
        if random_seed is not None:
            self.random_seed = random_seed
        else:
            self.random_seed = np.random.random_integers(0, 65536)
        # Список кластеров
        self.clusters = {}  # CCluster
        # Номера шумовых кластеров
        # Данный объект необходим для того, чтобы не брать во внимание те объкты, которые были отнесены к шумовым
        self.noise_clusters = {}
        # Количество добавленных транзакций
        self.count_transactions = 0
        # Номер итерации
        self.iteration = 0
        # Словарь. ключ/значение : номер транзакции/номер кластера
        self.transaction = {}
        # Максимальный номер кластера
        self.max_cluster_number = 0
        self.print_step = print_step
        self.is_save_history = is_save_history

    '''
    Рассчитывается изменение Goal, которое получит целевая функция при добавлении транзакции к кластеру clusterNumber.
    Кластер, доставляющий максимальное значение функции, будет искомым кластером (в который следует добавить
    транзакцию)
    Input parametres:
    transaction -- транзакция (список объектов)
    clusterNumber -- номер кластера, приращение для которого рассчитывается
    r -- отталкивание в смысле CLOPE
    Returned value:
    Возвращает значение изменения целевой функции при добавлении transaction к кластеру clusterNumber
    '''
    def delta_transaction(self, transaction, cluster_number, r):
        area = self.clusters[cluster_number].area + len(transaction)
        width = self.clusters[cluster_number].width
        for item in transaction:
            if not (item in self.clusters[cluster_number].histogram):
                width += 1
        if width != 0:
            new_delta_value = area * (self.clusters[cluster_number].count_transactions + 1) / (width ** r)
        else:
            new_delta_value = 0
        if self.clusters[cluster_number].width != 0:
            old_delta_value = self.clusters[cluster_number].area * self.clusters[cluster_number].count_transactions / (
                self.clusters[cluster_number].width ** r)
        else:
            old_delta_value = 0
        return new_delta_value - old_delta_value

    '''
    Функция удаления шума. Все кластеры, размер которых больше limit остаются
    Input parametres:
    limit -- уровень шума кластеров
    '''
    def noise_reduction(self, limit):
        # Удаляем все пустые и зашумлённые кластеры
        new_clusters = {}
        for item in self.clusters:
            if self.clusters[item].count_transactions > limit:
                new_clusters[item] = self.clusters[item]
            else:
                self.noise_clusters[item] = True
        self.clusters = new_clusters

    '''
    Вычисление целевой функции для всех уже сформированных кластеров
    Используется при модификации кластеров, либо их инициализации
    Input parametres:
    r -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    Returned value:
    Возвращает значение целевой функции
    '''
    def get_goal_function(self, r):
        measure = 0.0
        # Перебираем все кластеры и для каждого рассчитываем его вес. Все веса суммируются в общую метрику
        for item in self.clusters:
            if item.width == 0:
                # print "test"
                pass
            else:
                # Попытка подобрать иную метрику
                # measure += (r ** 2 * math.log(item.Area ** (1 / r) / item.Width) ** 2) *
                # item.CountTransactions / self.CountTransactions
                measure += item.area / (item.width ** r) * item.count_transactions / self.count_transactions
        return measure

    '''
    Добавление новой транзакции
    Пытаемся перераспределить транзакцию (transaction) с номером id в другой класс так, чтобы целевая функция приняла
    максимальное значение
    Input parametres:
    transaction -- транзакция (слайс с объектами)
    id -- номер транзакции
    repulsion -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    isSaveHistory -- флаг, выставляемый при необходимости записи истории количества транзакций
    Returned parameter:
    Возвращается номер кластера, в который была добавлена текущая транзакция
    '''
    def move_transaction(self, transaction, id, repulsion=2, max_count_clusters=None):
        r = repulsion
        max_value = None
        max_value_index = None
        self.count_transactions += 1

        # Ищем кластер, на котором будет достигнуто максимальное значение изменения целевой функции
        for cluster_number in self.clusters:
            # Пишем историю
            if self.is_save_history:
                self.clusters[cluster_number].history_count_transact.append(
                    self.clusters[cluster_number].count_transactions
                )

            delta = self.delta_transaction(transaction, cluster_number, r)
            if (delta > 0 or max_count_clusters is not None) and (max_value is None or delta > max_value):
                max_value_index = cluster_number
                max_value = delta

        # Добавляем транзакцию в новый кластер и смотрим на результат
        if max_count_clusters is None or len(self.clusters) < max_count_clusters:
            self.clusters[self.max_cluster_number] = Cluster(self.count_transactions)
            if max_value is None or self.delta_transaction(transaction, self.max_cluster_number, r) > max_value:
                max_value_index = self.max_cluster_number
                self.max_cluster_number += 1
            else:
                del self.clusters[self.max_cluster_number]

        # Запоминаем, в каком кластере лежит текущая транзакция
        self.transaction[id] = max_value_index

        # Добавляем транзакцию в необходимый кластер
        self.clusters[max_value_index].add_transaction(transaction)

        return max_value_index

    '''
    Адаптивное вычисление порога шума. Порог вычистывается относительно медианы размеров кластеров (в числе
    транзакций). Берётся 3/4 медианы
    '''
    def get_noise_limit(self, percentile=0.75):
        size_clusters = []
        for item in self.clusters:
            size_clusters.append(self.clusters[item].count_transactions)
        sorted(size_clusters)
        median_element = int(len(size_clusters) * percentile) + 1
        if len(size_clusters) < 5:
            limit = 10
        else:
            limit = size_clusters[median_element]
        return limit

    '''
    Инициализация кластеров
    Input parametres:
    data -- слайс с транзакциями
    isPrint -- нужно ли печатать информацию о ходе выполнения (0 -- не нужно, если > 0 -- печатаем каждый isPrint раз)
    repulsion -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    isSaveHistory -- флаг, выставляемый при необходимости записи истории количества транзакций
    isNoiseReduction -- подавление шума (порог соответствует числу элементов в кластере, при котором он уничтожается).
                        Если isNoiseReduction == -1, то порог выбирается адаптивно (всё то, что больше медианы
                        остаётся)
    '''
    def init_clusters(self, data, repulsion=2, is_noise_reduction=-1, noise_median_threshold=0.75,
                      max_count_clusters=None):
        index = 0
        keys = sorted(data.keys())
        np.random.seed(self.random_seed)
        np.random.shuffle(keys)
        for item in keys:
            self.move_transaction(data[item], item, repulsion, max_count_clusters)
            index += 1
            if self.print_step > 0 and index % self.print_step == 0:
                print("Итерация: ", self.iteration, ". Номер шага", index, ". Число кластеров: ", len(self.clusters))

        # Получаем оптимальный порог шума
        if is_noise_reduction < 0:
            is_noise_reduction = self.get_noise_limit(noise_median_threshold)
        # Удаляем все шумовые кластеры (после инициализации не бывает пустых классов, поэтому знак строго больше)
        if is_noise_reduction > 0:
            self.noise_reduction(is_noise_reduction)

        self.iteration = 1

    '''
    Выполнение алгоритма. Выполнение следующего шага
    Input parametres:
    data -- слайс с транзакциями
    isPrint -- нужно ли печатать информацию о ходе выполнения (0 -- не нужно, если > 0 -- печатаем каждый isPrint раз)
    repulsion -- вещественное число, обозначающие отталкивание кластеров в смысле CLOPE
    isSaveHistory -- флаг, выставляемый при необходимости записи истории количества транзакций
    isNoiseReduction -- подавление шума (порог соответствует числу элементов в кластере, при котором он уничтожается).
                        Если isNoiseReduction == -1, то порог выбирается адаптивно (всё то, что больше медианы
                        остаётся)
    Returned parameter:
    Возвращается число операций по перенесению транзакции из кластера в кластер
    '''
    def next_step(self, data, repulsion=2, is_noise_reduction=-1, noise_median_threshold=0.75, max_count_clusters=None):

        # Удаляем все пустые (или шумовые, если isNoiseReduction > 0) кластеры
        if is_noise_reduction < 0:
            is_noise_reduction = self.get_noise_limit(noise_median_threshold)
        self.noise_reduction(is_noise_reduction)

        index = 0
        # Количество транзакций, которые были переложены
        eps = 0
        keys = sorted(data.keys())
        np.random.seed(self.random_seed)
        np.random.shuffle(keys)
        for id in keys:
            # Смотрим, где данная транзакция лежит сейчас
            cluster_number = self.transaction[id]
            transaction = data[id]
            # Если транзакция относится к шумовому кластеру, то не пытаемся её поменять
            if cluster_number in self.noise_clusters:
                eps += 0
            else:
                # Извлекаем транзакцию из текущего кластера
                self.clusters[cluster_number].remove_transaction(transaction)
                # Рассматриваем транзакцию как вновь пришедшую и добавляем в тот кластер, где значение целевой
                # функции доставит максимум
                eps += int(
                    self.move_transaction(transaction, id, repulsion, max_count_clusters)
                    !=
                    cluster_number
                )

            index += 1
            if self.print_step is not None and self.print_step > 0 and index % self.print_step == 0:
                print("Итерация: ", self.iteration, ". Номер шага", index, ". Число кластеров: ", len(self.clusters))
        self.iteration += 1

        self.noise_reduction(is_noise_reduction)
        return eps

    '''
    Рисуем график, демонстрирующий количество транзакций в различных классах
    '''
    def print_history_count(self, repulsion, seed):
        # Длина всех векторов с историями одинакова. В связи с этим, берём длину первого
        len_history = len(list(self.clusters.values())[0].history_count_transact)
        for index_cluster in self.clusters:
            item_cluster = self.clusters[index_cluster]
            x = np.array(range(0, len_history))
            if len(item_cluster.history_count_transact) != 0:
                y = item_cluster.history_count_transact
            else:
                y = np.array(range(0, len_history))
            plt.plot(x, y)
        plt.xlabel(u"Номер итерации")
        plt.ylabel(u"Количество транзакций")
        plt.title(u"Количество транзакций в различных кластерах. \nКоличество кластеров: "+str(len(self.clusters))+
                  u".\n Отталкивание: "+str(repulsion)+". Seed: "+str(seed))
        plt.show()

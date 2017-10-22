# -*- coding: utf-8 -*-
import CLOPE
import json
import matplotlib.pyplot as plt

# Прочитываем данные
with open('data/clope_features.json', 'r') as f:
    clients = json.load(f)

# Начальные данные
repulsion = 2
is_save_hist = True
noise_limit = 0
max_count_clusters = None
random_state = 42

clope = CLOPE.CLOPE(print_step=5000, is_save_history=True)
# Инициализируем алгоритм
clope.init_clusters(clients, repulsion, noise_limit)
clope.print_history_count()
# Итерируемся
while clope.next_step(clients, repulsion, 500) > 0:
   clope.print_history_count()

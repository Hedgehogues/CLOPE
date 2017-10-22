import numpy as np
import CLOPE


f = open('data/access.log', 'r')
log = [item for item in f.readlines()]

# 207 уникальных ip
# Все таймзоны одинаковые
# Дни месяцев брать не будем

date = np.array([item.split()[3][1:].split('/') for item in log])

ip = [item.split()[0] + '_0' for item in log]
month = [month + '_1' for month in date[:, 1]]
year = [item.split(':')[0] + '_2' for item in date[:, 2]]
hour = [item.split(':')[1] + '_3' for item in date[:, 2]]
type_of_query = [item.split()[5] + '_4' for item in log]
proto = [item.split()[7] + '_5' for item in log]
code = [item.split()[8] + '_6' for item in log]
browse = [item.split()[11] + '_7' for item in log]
path = [[path for path in item.split()[6].split('/') if len(path) != 0] for item in log]

# trasactions = {i: transact for i, transact in enumerate(np.transpose(np.vstack([ip, month, year, hour, type_of_query, proto, code, browse])))}
trasactions = {i: transact for i, transact in enumerate(np.transpose(path))}

noiseLimit = 0
seed = 41
r = 1.4
clope = CLOPE.CLOPE(print_step=5000, is_save_history=True, random_seed=seed)
clope.init_clusters(trasactions, r, noiseLimit)
clope.print_history_count(r, seed)

while clope.next_step(trasactions, r, noiseLimit) > 0:
    clope.print_history_count(r, seed)



count = 0
cl = []
for transact_ind in clope.transaction:
    cluster = clope.transaction[transact_ind]
    if cluster == 6:
        cl.append(trasactions[transact_ind])
        count += 1
    if count > 20:
        break

print(cl)

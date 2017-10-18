import vk
import sys
import json
from time import sleep

with open('token') as file:
	token = file.read().rstrip()

session = vk.Session(access_token=token)
api = vk.API(session)

def get_groups(group_ids):
	count = 200
	offset = 0
	names = {}
	while len(group_ids[offset : offset + count]) > 0:
		response = api.groups.getById(group_ids=group_ids[offset : offset + count])
		sleep(1.0/3.0)
		for group in response:
			names[group["gid"]] = group["name"]
		offset += count
	return names

with open("groups_members") as file:
	groups_members = json.loads(file.read())

groups_members = dict(filter(lambda x: len(x[1]) > 1, groups_members.items()))

names = get_groups(list(groups_members.keys()))

for group, members in sorted(groups_members.items(), key=lambda x: len(x[1])):
	print("{} {} {}".format(len(members), group, names[int(group)]))

import json

with open("groups_members") as file:
	groups_members = json.loads(file.read())

users = {}

for group, members in groups_members.items():
	for user in members:
		users[user] = 1

print(len(users))

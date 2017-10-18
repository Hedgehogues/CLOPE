import vk
import random
import numpy.random as nprnd
import sys
import json
from time import sleep

def wait():
	sleep(1.0/3.0)

with open('token') as file:
	token = file.read().rstrip()

session = vk.Session(access_token=token)
api = vk.API(session)

def get_random_users(n):
	return nprnd.randint(423307000, size=n)

# TODO:
# def get_all(method, id):
def get_groups(user_id):
	units = []
	count = 200
	offset = 0
	size = 1
	while offset < size:
		response = api.groups.get(user_id=user_id, count=count, offset=offset)
		wait()
		size = response[0]
		units += response[1:]
		offset += count
	return units

try:
	with open("groups_members") as file:
		groups_members = json.loads(file.read())
except (FileNotFoundError, json.decoder.JSONDecodeError):
	groups_members = {}

for user_id in get_random_users(int(sys.argv[1])):
	print(user_id)
	try:
		for group_id in get_groups(user_id):
			if not str(group_id) in groups_members:
				groups_members[str(group_id)] = {}
			groups_members[str(group_id)][str(user_id)] = 1
	except vk.exceptions.VkAPIError:
		print("ошибочка") 

with open("groups_members", "w") as file:
	file.write(json.dumps(groups_members))

# print(groups_members)

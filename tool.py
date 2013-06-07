#!/usr/bin/env python
# -*- coding: utf-8 -*-

from RedisCommand import getRedisCommand

def string2int(string):
	try:
		return int(string)
	except ValueError:
		return string

def isRedisCommand(command):
	commands = getRedisCommand()

	arglist = command.split(' ')
	argv = len(arglist)
	commandType = arglist[0].lower()

	if commandType == 'config' and argv > 1 and arglist[1].lower() == 'set':
		return True
	if commandType == 'config' and argv > 1 and arglist[1].lower() == 'get':
		return True
	if commandType == 'del':
		return True
	else:
		return commandType in commands.keys()

# =================test==================== #
def test():
	print isRedisCommand("select * from book")
	print isRedisCommand("update xxxxxxxxxxx")
	print isRedisCommand("dbsize")
	print isRedisCommand("madan")

	print type(string2int("-1"))
	print type(string2int("asa"))

if __name__ == '__main__':
	test()
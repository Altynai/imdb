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

def formatRedisString(string):
	length = len(string)
	if length <= 1:
		return string
	if string[0] == '"' and string[-1] == '"':
		string = string[1:-1]
		return string

	if string[0] == "'" and string[-1] == "'":
		string = string[1:-1]
	return string

# =================test==================== #
def test():
	print isRedisCommand("select * from book")
	print isRedisCommand("update xxxxxxxxxxx")
	print isRedisCommand("dbsize")
	print isRedisCommand("madan")

	print type(string2int("-1"))
	print type(string2int("asa"))

	print formatRedisString("'\"12345\"'")
	print formatRedisString('"\'12345\'"')
	print formatRedisString("normal")

if __name__ == '__main__':
	test()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import sys
import re
import redis

def process(string):
	string = string.replace('\n', ' ')
	string = re.sub(" +", " ", string)
	return string.lower()

def getRedisCommand():
	commands = dict()
	commands.setdefault('auth', 1)
	commands.setdefault('bgrewriteaof', 0)
	commands.setdefault('bgsave', 0)
	commands.setdefault('bitcount', -1)
	commands.setdefault('blpop', -1)
	commands.setdefault('brpop', -1)
	commands.setdefault('decrby', 2)
	commands.setdefault('del', -1)
	commands.setdefault('exists', 1)
	commands.setdefault('expire', 2)
	commands.setdefault('expireat', 2)
	commands.setdefault('flushall', 0)
	commands.setdefault('flushdb', 0)
	commands.setdefault('getbit', 2)
	commands.setdefault('hdel', -1)
	commands.setdefault('hexists', 2)
	commands.setdefault('hgetall', 1)
	commands.setdefault('hincrbyfloat', 3)
	commands.setdefault('hlen', 1)
	commands.setdefault('hmset', -1)
	commands.setdefault('incrby', 2)
	commands.setdefault('incrbyfloat', 2)
	commands.setdefault('info', -1)
	commands.setdefault('lastsave', 0)
	commands.setdefault('linsert', 4)
	commands.setdefault('llen', 1)
	commands.setdefault('lpush', -1)
	commands.setdefault('lpushx', 2)
	commands.setdefault('lset', 3)
	commands.setdefault('ltrim', 3)
	commands.setdefault('move', 2)
	commands.setdefault('mset', -1)
	commands.setdefault('msetnx', -1)
	commands.setdefault('object', -1)
	commands.setdefault('persist', 1)
	commands.setdefault('ping', 0)
	commands.setdefault('psetex', 3)
	commands.setdefault('randomkey', 0)
	commands.setdefault('rename', 2)
	commands.setdefault('renamenx', 2)
	commands.setdefault('rpush', -1)
	commands.setdefault('rpushx', 2)
	commands.setdefault('sadd', -1)
	commands.setdefault('save', 0)
	commands.setdefault('scard', 1)
	commands.setdefault('sdiff', -1)
	commands.setdefault('sdiffstore', -1)
	commands.setdefault('select', 1)
	commands.setdefault('set', -1)
	commands.setdefault('setbit', 3)
	commands.setdefault('setex', 3)
	commands.setdefault('setnx', 2)
	commands.setdefault('setrange', 3)
	commands.setdefault('shutdown', -1)
	commands.setdefault('sinter', -1)
	commands.setdefault('sinterstore', -1)
	commands.setdefault('sismember', 2)
	commands.setdefault('slaveof', 2)
	commands.setdefault('smembers', 1)
	commands.setdefault('smove', 3)
	commands.setdefault('sort', -1)
	commands.setdefault('srem', -1)
	commands.setdefault('strlen', 1)
	commands.setdefault('sunion', -1)
	commands.setdefault('sunionstore', -1)
	commands.setdefault('time', 0)
	commands.setdefault('unwatch', 0)
	commands.setdefault('watch', -1)
	commands.setdefault('zadd', -1)
	commands.setdefault('zcard', 1)
	commands.setdefault('zincrby', 3)
	commands.setdefault('zrange', -1)
	commands.setdefault('zrangebyscore', -1)
	commands.setdefault('zrank', 2)
	commands.setdefault('zrem', -1)
	commands.setdefault('zremrangebyrank', 3)
	commands.setdefault('zremrangebyscore', 3)
	commands.setdefault('zrevrange', -1)
	commands.setdefault('zrevrangebyscore', -1)
	commands.setdefault('zrevrank', 2)
	commands.setdefault('zscore', 2)
	return commands

if __name__ == '__main__':
	sys.stdout = open("command.list", "w")
	url = "http://redis.io/commands"
	commandset = set(redis.StrictRedis.RESPONSE_CALLBACKS.keys()) # uppercase
	soup = BeautifulSoup(urllib.urlopen(url).read())
	for command in soup.find_all("span", class_ = "command"):
		strings = [process(str(x)) for x in command.stripped_strings]
		command = strings[0].upper() 

		if command in commandset:
			if len(strings) == 1:
				print "commands.setdefault('%s', 0)" % command.lower()
			else:
				args = strings[1]
				print "commands.setdefault('%s', %d)" % (command.lower(), -1 if args.find('[') != -1 else len(args.split()))

	print getRedisCommand()

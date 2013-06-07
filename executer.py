import redis
import logging
import time
import string
import random
import MySQLdb
import RedisCommand
from tool import string2int

loggerformat ='line:[%(lineno)d] %(asctime)s %(filename)s %(levelname)s %(message)s'

logging.basicConfig(format = loggerformat,
				filename = 'log/executer.log',
				filemode = 'w',
				level = logging.DEBUG)

class Executer(object):
	"""
	sql executer, execute redis's new command "sql":
	>>> sql "sql content"
	"""

	def __init__(self, host = 'localhost', port = 6379, db = 0):
		self.sqlredis = redis.StrictRedis(host, port, db)
		self.logger = logging.getLogger()
		self.redisCommands = RedisCommand.getRedisCommand()

	def executeSQL(self, command):
		"""
		if the sql works, return True, response(may be int, list...)
		if not, return False, response(a exception)
		"""
		try:
			response = self.sqlredis.sql(command)
			return True, response
		except Exception, e:
			self.logger.error(e)
			return False, e

	def executeRedis(self, command):
		"""
		if the redis works, return True, response(may be int, list...)
		if not, return False, response(a exception)
		"""
		arglist = [string2int(x) for x in command.split(' ')]
		argv = len(arglist)
		commandType = arglist[0].lower()

		# 
		if commandType == 'config' and argv > 1 and arglist[1].lower() == 'set':
			commandType, arglist = 'config_set', arglist[2:]
		elif commandType == 'config' and argv > 1 and arglist[1].lower() == 'get':
			commandType, arglist = 'config_get', arglist[2:]
		elif commandType == 'del':
			commandType, arglist = 'delete', arglist[1:]
		else:
			arglist = arglist[1:]

		if commandType in self.redisCommands.keys():
			argv = self.redisCommands.get(commandType)
			method = getattr(self.sqlredis, commandType)

			try:
				if argv == 0:
					result = method()
				elif argv == -1:
					result = method(*arglist)
				else:
					argv = argv if argv < len(arglist) else len(arglist)
					result = method(*(arglist[0:argv]))
				return True, result
			except Exception, e:
				return False, e
		else:
			return False, Exception("No method named %s()." % commandType)

	def splitCommandFile(self, filepath):
		"""
		if file contains a lot of command, they should be split by ';'
		such as

		file.command
		-----------------
		command1;\n
		command2;\n
		command3;\n
		EOF
		-----------------
		
		return [command1,command2,...]
		"""
		text = ""
		with open(filepath, "r") as fin:
			while True:
				line = fin.readline()
				if not line:
					break
				text += line
		return self.splitCommand(text)

	def splitCommand(self, text):
		"""
		if text contains a lot of command, they should be split by ';'
		such as

		text
		-----------------
		command1;\n
		command2;\n
		command3;\n
		-----------------
		
		return [command1,command2,...]
		"""
		commandlist = list()
		textlist = text.split('\n')
		size = len(textlist)
		index = 0

		while index < size:
			command = ""
			while index < size:
				line = textlist[index]
				index = index + 1
				line = line.strip(' \n')
				command = command + line
				if index >= size:
					if command:commandlist.append(command)
					break
				if line[-1:] == ';':
					if command:commandlist.append(command)
					break
		return commandlist
		

# =================test================= #

def testRedis(openIndex = False):
	sqler = Executer()
	genre_type = sqler.splitCommandFile("sql/genre_type_table.sql")
	movie_table = sqler.splitCommandFile("sql/movie_table.sql")
	cleanup = sqler.splitCommandFile("sql/cleanup.sql")

	for sql in genre_type:
		sqler.executeSQL(sql)
	for sql in movie_table:
		sqler.executeSQL(sql)

	redis_write = 0
	redis_read = 0
	write_count = 0
	for x in xrange(0, 6):
		movie_x =sqler.splitCommandFile("sql/movie/movie_%d.sql" % x)
		redis_start = time.time()
		for sql in movie_x:
			write_count += 1
			sqler.executeSQL(sql)
		redis_end = time.time()
		redis_write += redis_end - redis_start

	if openIndex:
		for x in xrange(0, 6):
			sqler.executeSQL("create index genre_index_%d on movie_%d(genre)" % (x, x))

	redis_start = time.time()
	for i in xrange(10000):
		sqler.executeSQL("select * from movie_0 where genre = %d" % random.randint(1,100000))
	redis_end = time.time()
	redis_read += redis_end - redis_start

	for sql in cleanup:
		sqler.executeSQL(sql)
	sqler.logger.info('redis witre:' + str(write_count) + " times")
	sqler.logger.info('redis witre:' + str(redis_write) + "s")
	sqler.logger.info('redis%s read:' % ("(With Index)" if openIndex else "") + str(redis_read) + "s")


def testMySQL():
	sqler = Executer()
	genre_type = sqler.splitCommandFile("sql/genre_type_table.sql")
	movie_table = sqler.splitCommandFile("sql/movie_table.sql")
	cleanup = sqler.splitCommandFile("sql/cleanup.sql")
	try:
		conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = '121212', db = 'redis', port = 3306)
		cur = conn.cursor()

		for sql in genre_type:
			cur.execute(sql)
		for sql in movie_table:
			cur.execute(sql)

		mysql_write = 0
		write_count = 0
		mysql_read = 0
		for x in xrange(0, 6):
			movie_x = sqler.splitCommandFile("sql/movie/movie_%d.sql" % x)
			mysql_start = time.time()
			for sql in movie_x:
				write_count += 1
				cur.execute(sql)
			conn.commit()
			mysql_end = time.time()
			mysql_write += mysql_end - mysql_start

		mysql_start = time.time()
		for i in xrange(10000):
			cur.execute("select * from movie_0 where genre = %d" % random.randint(1,100000))
		mysql_end = time.time()
		mysql_read += mysql_end - mysql_start

		for sql in cleanup:
			cur.execute(sql)
		sqler.logger.info('mysql write:' + str(write_count) + " times")
		sqler.logger.info('mysql write:' + str(mysql_write) + "s")
		sqler.logger.info('mysql read:' + str(mysql_read) + "s")
		conn.commit()

		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print e
	
	start = time.time()
	end = time.time()

	return end - start

def testRedisCommand():
	rediser = Executer()
	rediser.executeRedis('FLUSHALL')
	rediser.executeRedis('RPUSH mylist b')
	rediser.executeRedis('RPUSH mylist b')
	rediser.executeRedis('RPUSH mylist b')
	rediser.executeRedis('RPUSH mylist a')
	rediser.executeRedis('LREM mylist 0 a')
	print rediser.executeRedis('LRANGE mylist 0 -1')

if __name__ == '__main__':
	"""
	just test:)
	"""
	# testMySQL()
	# testRedis()
	# testRedis(True)
	testRedisCommand()

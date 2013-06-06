import redis
import logging
import time
import string
import random
import MySQLdb

loggerformat ='line:[%(lineno)d] %(asctime)s %(filename)s %(levelname)s %(message)s'

logging.basicConfig(format = loggerformat,
				filename = 'log/executer.log',
				filemode = 'w',
				level = logging.DEBUG)

class sqlexecuter(object):
	"""
	sql executer, execute redis's new command "sql":
	>>> sql "sql content"
	"""

	def __init__(self, host = 'localhost', port = 6379, db = 0):
		self.sqlredis = redis.StrictRedis(host, port, db)
		self.logger = logging.getLogger()

	def execute_sql(self, sqlcontent):
		"""
		if the sql works, return True, response(may be int, list...)
		if not, return False, response(a exception)
		"""
		try:
			response = self.sqlredis.sql(sqlcontent)
			return True, response
		except Exception, e:
			self.logger.error(e)
			return False, e

	def split_sql_file(self, filepath):
		"""
		if file contains a lot of sql, they should be split by ';'
		such as

		file.sql
		-----------------
		sql1;\n
		sql2;\n
		sql3;\n
		EOF
		-----------------
		
		return [sql1,sql2,...]
		"""
		sqllist = list()
		with open(filepath, "r") as fin:
			sql = ""
			fileEOF = False
			while not fileEOF:
				sql = ""
				while not fileEOF:
					line = fin.readline()
					if not line:
						if sql:sqllist.append(sql)
						fileEOF = True
						break
					line = line.strip(' \n')
					sql = sql + line
					if line[-1:] == ';':
						if sql:sqllist.append(sql)
						break
		return sqllist

	def split_sql_text(self, text):
		"""
		if text contains a lot of sql, they should be split by ';'
		such as

		text
		-----------------
		sql1;\n
		sql2;\n
		sql3;\n
		-----------------
		
		return [sql1,sql2,...]
		"""
		sqllist = list()
		textlist = text.split('\n')
		size = len(textlist)
		index = 0

		while index < size:
			sql = ""
			while index < size:
				line = textlist[index]
				index = index + 1
				line = line.strip(' \n')
				sql = sql + line
				if index >= size:
					if sql:sqllist.append(sql)
					break
				if line[-1:] == ';':
					if sql:sqllist.append(sql)
					break
		return sqllist




# =================test================= #

def testRedis(openIndex = False):
	sqler = sqlexecuter()
	genre_type = sqler.split_sql_file("sql/genre_type_table.sql")
	movie_table = sqler.split_sql_file("sql/movie_table.sql")
	cleanup = sqler.split_sql_file("sql/cleanup.sql")

	for sql in genre_type:
		sqler.execute_sql(sql)
	for sql in movie_table:
		sqler.execute_sql(sql)

	redis_write = 0
	redis_read = 0
	write_count = 0
	for x in xrange(0, 6):
		movie_x =sqler.split_sql_file("sql/movie/movie_%d.sql" % x)
		redis_start = time.time()
		for sql in movie_x:
			write_count += 1
			sqler.execute_sql(sql)
		redis_end = time.time()
		redis_write += redis_end - redis_start

	if openIndex:
		for x in xrange(0, 6):
			sqler.execute_sql("create index genre_index_%d on movie_%d(genre)" % (x, x))

	redis_start = time.time()
	for i in xrange(10000):
		sqler.execute_sql("select * from movie_0 where genre = %d" % random.randint(1,100000))
	redis_end = time.time()
	redis_read += redis_end - redis_start

	for sql in cleanup:
		sqler.execute_sql(sql)
	sqler.logger.info('redis witre:' + str(write_count) + " times")
	sqler.logger.info('redis witre:' + str(redis_write) + "s")
	sqler.logger.info('redis%s read:' % ("(With Index)" if openIndex else "") + str(redis_read) + "s")


def testMySQL():
	sqler = sqlexecuter()
	genre_type = sqler.split_sql_file("sql/genre_type_table.sql")
	movie_table = sqler.split_sql_file("sql/movie_table.sql")
	cleanup = sqler.split_sql_file("sql/cleanup.sql")
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
			movie_x = sqler.split_sql_file("sql/movie/movie_%d.sql" % x)
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

if __name__ == '__main__':
	"""
	just test:)
	"""
	testMySQL()
	testRedis()
	testRedis(True)

import redis
import logging
import time
import MySQLdb

loggerformat ='line:[%(lineno)d] %(asctime)s %(filename)s %(levelname)s %(message)s'

logging.basicConfig(format = loggerformat,
				filename = 'log/sqlexecuter.log',
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

	def splie_sql_file(self, filepath):
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

	def select(self, sqlcontent):
		return self.execute_sql(sqlcontent)

	def update(self, sqlcontent):
		return self.execute_sql(sqlcontent)

	def insert(self, sqlcontent):
		return self.execute_sql(sqlcontent)

	def create(self, sqlcontent):
		return self.execute_sql(sqlcontent)

	def drop(self, sqlcontent):
		return self.execute_sql(sqlcontent)


def test():
	try:
		sqler = sqlexecuter()
		genre_type = sqler.splie_sql_file("sql/genre_type_table.sql")
		movie_table = sqler.splie_sql_file("sql/movie_table.sql")
		movie_0 =sqler.splie_sql_file("sql/movie/movie_0.sql")
		cleanup = sqler.splie_sql_file("sql/cleanup.sql")

		redis_start = time.time()
		for sql in genre_type:
			sqler.execute_sql(sql)
		for sql in movie_table:
			sqler.execute_sql(sql)
		for sql in movie_0:
			sqler.execute_sql(sql)
		redis_end = time.time()
		for sql in cleanup:
			sqler.execute_sql(sql)
		sqler.logger.info('redis:' + str(redis_end - redis_start) + "s")
		

		conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd = '121212',db = 'redis',port = 3306)
		cur = conn.cursor()
		mysql_start = time.time();

		for sql in genre_type:
			cur.execute(sql)
		for sql in movie_table:
			cur.execute(sql)
		for sql in movie_0:
			cur.execute(sql)
		mysql_end = time.time()
		for sql in cleanup:
			cur.execute(sql)

		conn.commit()
		sqler.logger.info('mysql:' + str(mysql_end - mysql_start) + "s")

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
	test()

import MySQLdb

prime = 103

try:
	count = 1
	connection = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '121212', db = 'imdb')
	cur = connection.cursor()
	for i in xrange(prime):
		with open('sql/movie/movie_%d.sql' % i, 'r') as fin:
			while True:
				line = fin.readline()
				if line:
					cur.execute(line)
					print '%d processing..' % count
					print line
					count += 1
				else:
					break
	connection.commit()
	cur.close()
	connection.close()


except Exception, e:
	raise e
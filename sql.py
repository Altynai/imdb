import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

try:
	print r.sql("update k set gener = 24 where gener = 299")
except Exception, e:
	print e
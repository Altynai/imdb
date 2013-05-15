import sys

prime = 103
template = """drop table if exists movie_%d;
create table movie_%d(
	name varchar(50) not null,
	year varchar(10) not null,
	genre int
);
"""

sys.stdout = open('sql/movie_table.sql', 'w')
for i in xrange(prime):
	print template % (i, i)


import sys

prime = 11
template = """drop table if exists movie_%d;
create table movie_%d(
	name varchar(150) not null,
	year varchar(20) not null,
	genre int
);
"""

sys.stdout = open('movie_table.sql', 'w')
for i in xrange(prime):
	print template % (i, i)


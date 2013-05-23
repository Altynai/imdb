import string
import mmhash
import sys



genre_dict = dict()
genre_dict.setdefault('Sci-Fi', 0)
genre_dict.setdefault('Crime', 1)
genre_dict.setdefault('Romance', 2)
genre_dict.setdefault('Animation', 3)
genre_dict.setdefault('Music', 4)
genre_dict.setdefault('Adult', 5)
genre_dict.setdefault('Comedy', 6)
genre_dict.setdefault('War', 7)
genre_dict.setdefault('Horror', 8)
genre_dict.setdefault('Film-Noir', 9)
genre_dict.setdefault('Adventure', 10)
genre_dict.setdefault('News', 11)
genre_dict.setdefault('Reality-TV', 12)
genre_dict.setdefault('Thriller', 13)
genre_dict.setdefault('Western', 14)
genre_dict.setdefault('Mystery', 15)
genre_dict.setdefault('Short', 16)
genre_dict.setdefault('Lifestyle', 17)
genre_dict.setdefault('Talk-Show', 18)
genre_dict.setdefault('Drama', 19)
genre_dict.setdefault('Action', 20)
genre_dict.setdefault('Documentary', 21)
genre_dict.setdefault('Musical', 22)
genre_dict.setdefault('Experimental', 23)
genre_dict.setdefault('History', 24)
genre_dict.setdefault('Family', 25)
genre_dict.setdefault('Fantasy', 26)
genre_dict.setdefault('Game-Show', 27)
genre_dict.setdefault('Sport', 28)
genre_dict.setdefault('Biography', 29)

def check(x):
	return x == '-' or x in string.ascii_lowercase or x in string.ascii_uppercase

def split(line):
	n = len(line)
	top = 0
	stack = ['' for i in xrange(n)]
	flag = False

	name = ""
	year = ""
	i = 0
	while i < n:
		if flag == False:
			if line[i] == '(' and (line[i+1] == '?' or line[i+1] in string.digits):
				i += 1
				while line[i] != ')':
					year += line[i]
					i += 1
				flag = True
			else:
				name += line[i]
		else:
			break
		i += 1

	genre = ""
	id = n - 2
	while check(line[id:id+1]):
		genre = line[id] + genre
		id -= 1
	return name.replace('"', '').replace('\\','\\\\').strip(), year, genre_dict.get(genre)

prime = 11
template = """insert into movie_%d values("%s", "%s", %d);\n"""


sqlwrite = []
for i in xrange(prime):
	sqlwrite.append(open('movie/movie_%d.sql' % i, 'w'))


with open('test.list', 'r') as fin:
	lastname = ""
	lastyear = ""
	lasttableid = 0
	mask = 0
	row = 1
	while True:
		line = fin.readline()
		if line:
			print '%d processing..' % row
			row += 1
			
			name, year, genre = split(line)
			tableid = mmhash.get_unsigned_hash(name) % prime
			
			if lastname == "":
				lastname, lasttableid, lastyear, mask = name, tableid, year, 0

			if name == lastname:
				mask |= (1 << genre)
			else:
				sqlwrite[lasttableid].write(template % (lasttableid, lastname, lastyear, mask));
				lastname, lasttableid, lastyear, mask = name, tableid, year, (1 << genre)

		else:
			sqlwrite[lasttableid].write(template % (lasttableid, lastname, lastyear, mask));
			break

for i in xrange(prime):
	sqlwrite[i].close()
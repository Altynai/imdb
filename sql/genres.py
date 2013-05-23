
import string

genres = set()

def check(x):
	return x == '-' or x in string.ascii_lowercase or x in string.ascii_uppercase

with open('genres.backup', 'r') as fin:
	while True:
		line = fin.readline()
		if line:
			genre = ""
			id = len(line) - 2
			while check(line[id:id+1]):
				genre = line[id] + genre
				id -= 1
			genres.add(genre)
		else:
			break

for index, genre in enumerate(genres):
	# print "insert into imdb.genre_type values(%d, '%s');" % (index, genre)
	print "genre_dict.setdefault('%s', %d)" % (genre, index)

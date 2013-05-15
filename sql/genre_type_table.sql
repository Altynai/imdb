drop table if exists imdb.genre_type;

create table imdb.genre_type(
	type_id int primary key not null,
	type_name varchar(15) not null
);

insert into imdb.genre_type values(0, 'Sci-Fi');
insert into imdb.genre_type values(1, 'Crime');
insert into imdb.genre_type values(2, 'Romance');
insert into imdb.genre_type values(3, 'Animation');
insert into imdb.genre_type values(4, 'Music');
insert into imdb.genre_type values(5, 'Adult');
insert into imdb.genre_type values(6, 'Comedy');
insert into imdb.genre_type values(7, 'War');
insert into imdb.genre_type values(8, 'Horror');
insert into imdb.genre_type values(9, 'Film-Noir');
insert into imdb.genre_type values(10, 'Adventure');
insert into imdb.genre_type values(11, 'News');
insert into imdb.genre_type values(12, 'Reality-TV');
insert into imdb.genre_type values(13, 'Thriller');
insert into imdb.genre_type values(14, 'Western');
insert into imdb.genre_type values(15, 'Mystery');
insert into imdb.genre_type values(16, 'Short');
insert into imdb.genre_type values(17, 'Lifestyle');
insert into imdb.genre_type values(18, 'Talk-Show');
insert into imdb.genre_type values(19, 'Drama');
insert into imdb.genre_type values(20, 'Action');
insert into imdb.genre_type values(21, 'Documentary');
insert into imdb.genre_type values(22, 'Musical');
insert into imdb.genre_type values(23, 'Experimental');
insert into imdb.genre_type values(24, 'History');
insert into imdb.genre_type values(25, 'Family');
insert into imdb.genre_type values(26, 'Fantasy');
insert into imdb.genre_type values(27, 'Game-Show');
insert into imdb.genre_type values(28, 'Sport');
insert into imdb.genre_type values(29, 'Biography');
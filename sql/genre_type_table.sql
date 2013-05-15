drop table if exists genre_type;

create table genre_type(
	type_id int primary key not null,
	type_name varchar(15) not null
);

insert into genre_type values(0, 'Sci-Fi');
insert into genre_type values(1, 'Crime');
insert into genre_type values(2, 'Romance');
insert into genre_type values(3, 'Animation');
insert into genre_type values(4, 'Music');
insert into genre_type values(5, 'Adult');
insert into genre_type values(6, 'Comedy');
insert into genre_type values(7, 'War');
insert into genre_type values(8, 'Horror');
insert into genre_type values(9, 'Film-Noir');
insert into genre_type values(10, 'Adventure');
insert into genre_type values(11, 'News');
insert into genre_type values(12, 'Reality-TV');
insert into genre_type values(13, 'Thriller');
insert into genre_type values(14, 'Western');
insert into genre_type values(15, 'Mystery');
insert into genre_type values(16, 'Short');
insert into genre_type values(17, 'Lifestyle');
insert into genre_type values(18, 'Talk-Show');
insert into genre_type values(19, 'Drama');
insert into genre_type values(20, 'Action');
insert into genre_type values(21, 'Documentary');
insert into genre_type values(22, 'Musical');
insert into genre_type values(23, 'Experimental');
insert into genre_type values(24, 'History');
insert into genre_type values(25, 'Family');
insert into genre_type values(26, 'Fantasy');
insert into genre_type values(27, 'Game-Show');
insert into genre_type values(28, 'Sport');
insert into genre_type values(29, 'Biography');
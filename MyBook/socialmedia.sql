CREATE DATABASE socialmedia;
use socialmedia;
#Changed user_id to integer NOT NULL for all tables except User
#Changed user_id for user table to integer NOT NULL AUTO_INCREMENT,
#Changed profile_id for only profile table to integer NOT NULL AUTO_INCREMENT,
#Changed image_id for only image table to integer NOT NULL AUTO_INCREMENT,
#Changed profile_id for profile_id,image_id to integer NOT NULL,
#Changed dob to date in Profile

create table User(
	user_id integer NOT NULL AUTO_INCREMENT, 
	firstname varchar(100) NOT NULL,
	lastname varchar(100) NOT NULL,
	email varchar(100) NOT NULL,
	password_digest varchar(255) NOT NULL,
	primary key(user_id) 

);

create table Phone(
	user_id integer NOT NULL,
	telephone_no varchar(50) NOT NULL,
	area_code varchar(10) NOT NULL,
	
	primary key(user_id,telephone_no,area_code),

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade
);


create table Address(
	user_id integer NOT NULL,
	street_name varchar(100) NOT NULL,
	city varchar(100) NOT NULL,
	country varchar(50) NOT NULL,

	primary key(user_id, street_name, city, country),

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade
);

create table Profile(
	profile_id integer NOT NULL AUTO_INCREMENT,
	user_id integer,
	dob date,
	gender varchar(9),
	nickname varchar(100),

	primary key(profile_id, user_id),

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade
);



create table Image(
	image_id integer NOT NULL AUTO_INCREMENT,
	image_name varchar(50) NOT NULL,
	directory varchar(100) NOT NULL,

	primary key(image_id)
);

create table Profile_pic(
	profile_id integer NOT NULL,
	image_id integer NOT NULL,

	primary key(profile_id,image_id),

	foreign key(image_id)
	references Image(image_id) on delete cascade on update cascade,

	foreign key(profile_id)
	references Profile(profile_id) on delete cascade on update cascade

);

create table Adds(
	image_id integer NOT NULL,
	user_id integer NOT NULL,

	primary key(image_id),

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade,

	foreign key(image_id)
	references Image(image_id) on delete cascade on update cascade
);



create table Post(
	post_id integer NOT NULL AUTO_INCREMENT, 
	description varchar(250) NOT NULL,
	post_date date NOT NULL,
	post_time time NOT NULL,

	primary key(post_id)
);


create table Post_image(
	post_id integer NOT NULL,
	image_id integer NOT NULL,

	primary key(post_id, image_id),

	foreign key(post_id)
	references Post(post_id) on delete cascade on update cascade,

	foreign key(image_id)
	references Image(image_id) on delete cascade on update cascade
);


create table Submits(
	post_id integer NOT NULL,
	user_id integer NOT NULL,

	primary key(post_id),

	foreign key(post_id)
	references Post(post_id) on delete cascade on update cascade,

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade

);

create table Comment(
	com_id integer NOT NULL AUTO_INCREMENT, 
	post_id integer NOT NULL,
	usr_text varchar(250) NOT NULL,
	com_date date NOT NULL,
	com_time time NOT NULL,

	primary key(com_id,post_id),

	foreign key(post_id)
	references Post(post_id) on delete cascade on update cascade
);


create table Commented(
	user_id integer NOT NULL,
	com_id integer NOT NULL,
	post_id integer NOT NULL,

	primary key(user_id,com_id),

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade,

	foreign key(com_id)
	references Comment(com_id) on delete cascade on update cascade,

	foreign key(post_id)
	references Post(post_id) on delete cascade on update cascade
);


create table Group1(
	group_id integer NOT NULL AUTO_INCREMENT, 
	group_name varchar(50),

	primary key(group_id)
);

create table friends_with(
	user_id integer NOT NULL,
	friend_id integer NOT NULL,
	group_id integer NOT NULL,

	primary key(user_id,friend_id, group_id),

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade,
	
	foreign key(group_id)
	references Group1(group_id) on delete cascade on update cascade
);

create table creates(
	editor_id integer NOT NULL,
	group_id integer NOT NULL,
	user_id integer NOT NULL,
	create_date date,

	primary key(editor_id, group_id),

	foreign key(group_id)
	references Group1(group_id) on delete cascade on update cascade,

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade
);


create table joins(
	user_id integer NOT NULL,
	group_id integer NOT NULL,
	join_date date,

	primary key(user_id, group_id),

	foreign key(group_id)
	references Group1(group_id) on delete cascade on update cascade,

	foreign key(user_id)
	references User(user_id) on delete cascade on update cascade

);

create table belongs(
	post_id integer NOT NULL,
	group_id integer NOT NULL,

	primary key(post_id,group_id),

	foreign key(post_id)
	references Post(post_id) on delete cascade on update cascade,

	foreign key(group_id)
	references Group1(group_id) on delete cascade on update cascade
);

INSERT INTO Group1(group_id,group_name) VALUES(1,"Relatives");
INSERT INTO Group1(group_id,group_name) VALUES(2,"School");
INSERT INTO Group1(group_id,group_name) VALUES(3,"Work");
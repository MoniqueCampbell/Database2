use socialmedia;

# POST FEED TO DISPLAY ALL POSTS IN BY FRIENDS IN YOUR FRIEND GROUP ----------------------

Drop procedure IF EXISTS find_friends;
#SEARCH FOR FRIENDS USING ENTERED STING
delimiter //
CREATE PROCEDURE find_friends (IN name1 varchar(50))
	BEGIN
		select user.firstname, u2.firstname as friends from User join friends_with join user as u2 
		on user.user_id = friends_with.user_id and friends_with.friend_id = u2.user_id  where user.firstname LIKE CONCAT('%', name1,'%') or user.lastname LIKE CONCAT('%', name1,'%');
	END//
delimiter ;


drop procedure IF EXISTS friends_id;
#FIND ALL FRIENDS FOR A USER
delimiter //
CREATE PROCEDURE friends_id (IN userid int)
	BEGIN
		DROP TEMPORARY TABLE IF EXISTS temp_table;
        #creates a temporary table to create result of procedure
        CREATE TEMPORARY TABLE temp_table
		select friend_id, group_id from friends_with where user_id = userid order by user_id asc;
	END//
delimiter ;

drop procedure IF EXISTS all_friends_postid;
#Get all the post made by friend of user
delimiter //
CREATE PROCEDURE all_friends_postid (IN userid int)
	BEGIN
		CALL friends_id (userid); #creates temporary table temp_table to use in query below
        
        DROP TEMPORARY TABLE IF EXISTS PID;
        #creates a temporary table to create result of procedure
        CREATE TEMPORARY TABLE PID
		select belongs.post_id, belongs.group_id from submits join belongs join temp_table on belongs.post_id = submits.post_id and temp_table.friend_id = submits.user_id
		where temp_table.friend_id = user_id and belongs.group_id = temp_table.group_id;
        
        #SELECT post.post_id FROM post join PID on post.post_id = PID.post_id;
		SELECT post_id,description,post_date,post_time FROM Post WHERE post_id in (SELECT post.post_id FROM post join PID on post.post_id = PID.post_id) ORDER BY post_date DESC, post_time DESC;
	END//
delimiter ;


#DISPLAY ALL THE POST ON PROFILE PAGE AND WHERE ON BY USER IN YOUR THE FRIEND GROUP-----------------------
drop procedure IF EXISTS  view_firends_profile_post;
delimiter //
CREATE PROCEDURE view_firends_profile_post (IN uid int, IN fid int)
	BEGIN
		DROP TEMPORARY TABLE IF EXISTS fp;
		DROP TEMPORARY TABLE IF EXISTS fg;
		DROP TEMPORARY TABLE IF EXISTS ug;

		#select all posts made by users's friend
		CREATE TEMPORARY TABLE fp  Select post_id from submits where user_id = fid;
        
        #select all group that user and friends are in together
		CREATE TEMPORARY TABLE ug Select group_id from friends_with where user_id = uid and friend_id = fid;

		#select the post the friends made in post in
		CREATE TEMPORARY TABLE fg Select post_id from belongs where post_id in (SELECT * FROM fp) and group_id in (SELECT * FROM ug);

		#all posts in the friends (uid and Fid) groups
		SELECT * FROM Post where post_id in (Select * FROM fg);
        
	END//
delimiter ;

Call view_firends_profile_post(1, 10);


# TEST ---------------------------------------------
Call all_friends_postid (1); #returns PID with post_id of all the post made by friends.
Call all_friends_postid (10);

DROP TEMPORARY TABLE IF EXISTS A;
DROP TEMPORARY TABLE IF EXISTS B;
CREATE TEMPORARY TABLE A Select post_id from submits where user_id = 1;
CREATE TEMPORARY TABLE B Select group_id from friends_with where user_id = 10 and friend_id = 1;
Select post_id from belongs where post_id in (SELECT * FROM A) and group_id in (SELECT * FROM B);
SELECT * FROM A;
SELECT * FROM B;
#SET @fp := (Select post_id from submits where user_id = 10);
#SELECT @fp;

#not in use
drop view IF EXISTS friend_groups_view;
CREATE VIEW friend_groups_view AS
SELECT group_id
FROM group1
WHERE group_id in (1,2,3);




























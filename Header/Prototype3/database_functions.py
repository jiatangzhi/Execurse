import sqlite3 as sl

#Database functions for the login system

def check_username_already_used(username):
	'''
	Checks if the username is already registered on the database.
	Arguments: 
		username(str): username entered on signup
	Returns: 
		True if the user already exists, False otherwise
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT username FROM USER WHERE username = ?"""
	cursor.execute(query, [username])
	result = cursor.fetchall()
	cursor.close()

	if len(result) == 0:
		return False
	else:
		return True

def check_email_already_used(email):
	'''
	Checks if the email is already registered to a user on the database.
	Arguments: 
		email(str): email entered on signup
	Returns: 
		True if the email is already being used, False otherwise
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT email FROM USER WHERE email = ?"""
	cursor.execute(query, [email])
	result = cursor.fetchall()
	cursor.close()

	if len(result) == 0:
		return False
	else:
		return True

def add_user(username, passwordHash, email, accountType):
	'''
	Inputs the user's credentials into the database.
	Arguments:
		username(str): username entered on signup
		passwordHash(str): the password entered on signup salted and hashed
		email(str): the email entered on signup
		accountType(int): 1 for academic account, 0 for student account
	Returns: 
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO USER (username, password, email, academic)
	VALUES (?, ?, ?, ?)"""
	cursor.execute(query, [username, passwordHash, email, accountType])
	con.commit()
	cursor.close()

def get_password_hash(username):
	'''
	Gets the hashed password from the database of the user trying to login.
	Arguments:
		username(str): username entered during login
	Returns:
		passwordHash(str): hashed password acquired from the database
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT password FROM USER where username = ?"""
	cursor.execute(query, [username])
	result = cursor.fetchall()
	cursor.close()
	passwordHash = result[0][0]
	return passwordHash

def get_user_id(username):
	'''
	Gets the user_id from the database of the user who has logged in.
	Arguments:
		username(str): username entered during login
	Returns:
		user_id(int): user_id of the logged in user
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT user_id FROM USER where username = ?"""
	cursor.execute(query, [username])
	result = cursor.fetchall()
	cursor.close()
	user_id = result[0][0]
	return user_id

def get_user_type(username):
	'''
	Gets the account type from the database of the user who has logged in.
	Arguments:
		username(str): username entered during login
	Returns:
		accountType(int): 1 for academic account, 0 for student account
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT academic FROM USER where username = ?"""
	cursor.execute(query, [username])
	result = cursor.fetchall()
	cursor.close()
	accountType = result[0][0]
	return accountType

#Database functions for the support network

def add_to_support_network(userid, email, firstname, lastname, relation):
	'''
	Inputs the information of the person that the user wants to add to their support
	network into the database.
	Arguments:
		userid(int): the userid of the user currently logged in
		email(str): the email entered on the support network form
		firstname(str): the first name of the person entered on the form
		lastname(str): the last name of the person entered on the form
		relation(str): how the person entered and the user are related
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO SUPPORT_EMAILS (user_id, support_email, firstname, lastname, relation) 
	VALUES (?,?,?,?,?)"""
	cursor.execute(query, [userid, email, firstname, lastname, relation])
	con.commit()
	cursor.close()

def get_support_network(userid):
	'''
	Gets all the people registered to the current user's support network.
	Arguments:
		userid(int): the userid of the user currently logged in
	Returns:
		result(list of tuples): all records found from the database using the userid
			email_id(int): unique identifier for this entity
			user_id(int): foreign key which relates the users to the support network
			support_email(str): email of the person
			firstname(str): firstname of the person 
			lastname(str): lastname of the person
			relation(str): how the person and the user are related 
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM SUPPORT_EMAILS where user_id = ?"""
	cursor.execute(query, [userid])
	result = cursor.fetchall()
	cursor.close()
	return result

def delete_from_support_network(emailid):
	'''
	Deletes an email from the user's support network.
	Arguments:
		emailid(int): the unique identifier for the email the user wants to delete.
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """DELETE FROM SUPPORT_EMAILS WHERE email_id = ?"""
	cursor.execute(query, [emailid])
	con.commit()
	cursor.close()

def check_support_network(userid, email):
	'''
	Checks the support network to see if the email is already registered to the
	user currently logged in.
	Arguments:
		userid(int): the userid of the user currently logged in
		email(str): the email the user wants to add to the support network
	Returns:
		result(list of tuples): returns empty list if the email is not registered
			support_email(str): the emails found from the database query
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT support_email FROM SUPPORT_EMAILS WHERE 
	user_id = ? AND support_email = ?"""
	cursor.execute(query, [userid, email])
	result = cursor.fetchall()
	cursor.close()
	return result

def get_userid_email(emailid):
	'''
	Gets the userid of the emailid that the user wants to delete so only that
	user has permission to delete that email.
	Arguments:
		emailid(int): the emailid of the email that the user wants to delete
	Returns:
		result(list of tuples): will only contain the userid of a single record
			user_id(int): the userid attached to the email the user wants to delete
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT user_id FROM SUPPORT_EMAILS WHERE email_id = ?"""
	cursor.execute(query, [emailid])
	result = cursor.fetchall()
	cursor.close()
	return result

#Database functions for the leaderboard and gamification

def get_scores():
	'''Gets the scores of each user in descending order so the highest scorer
	is returned first and also does not get records where the score is 0.
	Arguments:
		Nothing
	Returns:
		result(list of tuples): returns empty list if everyone has 0 points
			username(str): the username that will be displayed on the leaderboard
			current_points(int): the current score of the user
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT username, current_points FROM USER WHERE current_points > 0 
	ORDER BY current_points DESC"""
	cursor.execute(query)
	result = cursor.fetchall()
	con.close()
	return result

def get_user_score(userid):
	'''Get the score of the user currently logged in so the score can be updated
	when the user scores points of the application.
	Arguments:
		userid(int): the userid of the user currently logged in
	Returns:
		result(list of tuples):
			current_points(int): the current score of the user
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = "SELECT current_points FROM USER WHERE user_id = ?"""
	cursor.execute(query, [userid])
	result = cursor.fetchall()
	con.close()
	return result

def change_user_score(userid, points):
	'''Changes the score of the user and updates the point total that is currently
	scored in the database.
	Arguments:
		userid(int): the userid of the user currently logged in
		points(int): the amount of points the user had just scored
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """UPDATE USER SET current_points = ? WHERE user_id = ?"""
	cursor.execute(query, [points, userid])
	con.commit()
	con.close()

#Datebase functions for the main forum page

def create_new_forum(forum_name):
	'''Creates a new subforum on the application and stores the name of the forum
	in the database.
	Arguments:
		forum_name(str): the name of the subforum the user wants to create
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO FORUMS (forum_name)
	VALUES(?)"""
	cursor.execute(query, [forum_name])
	con.commit()
	con.close()

def get_all_forums():
	'''Gets all the subforums that are stored in the database to be displayed on 
	the main forum page so the user can navigate to each subforum.
	Arguments:
		Nothing
	Returns:
		result(list of tuples):
			forum_name(str): the name of the subforum
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM FORUMS"""
	cursor.execute(query)
	result = cursor.fetchall()
	con.close()
	return result

def delete_forum(forum_name):
	'''Deletes a subforum from the main forum page.
	Arguments:
		forum_name(str): the name of the subforum the user wants to delete
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """DELETE FROM FORUMS WHERE forum_name = ?"""
	cursor.execute(query, [forum_name])
	con.commit()
	con.close()

def check_duplicate_forum(forum_name):
	'''Checks the database to see if the name of the subforum the user wants
	to create already exists within the database.
	Arguments:
		forum_name(str): the name of the subforum the user wants to create
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT forum_name FROM FORUMS WHERE forum_name = ?"""
	cursor.execute(query, [forum_name])
	result = cursor.fetchall()
	con.close()
	if len(result) == 0:
		return False
	else:
		return True

#Database functions for posting on the forum

def add_post(userid, author, forum, title, link, description, date, likes):
	'''Creates a new post on a specific subforum and stores it in the database.
	Arguments:
		userid(int): the userid of the user who has created the post
		author(str): the username of the user who has created the post
		forum(str): the name of the subforum the user is making the post on
		title(str): the title of the post
		link(str): a link that the user has attached to the post
		description(str): the content the user has provided in the post
		date(str): the current date/time that the user made the post
		likes(int): the amount of likes the post has (defaulted to 0)
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO POSTS (user_id, author, forum_name, title, link, content,
	created_at, likes) VALUES (?,?,?,?,?,?,?,?)"""
	cursor.execute(query, [userid, author, forum, title, link, description, date, likes])
	con.commit()
	cursor.close()

def get_posts(name):
	'''Gets all the posts that have been made of a specific subforum ordered by the
	date in which the post has been created (most recently appear first).
	Arguments:
		name(str): the name of the subforum that the user is currently on
	Returns:
		result(list of tuples):
			user_id(int): the userid of the user who has created the post
			author(str): the username of the user who has created the post
			forum_name(str): the name of the subforum the user made the post on
			title(str): the title of the post
			link(str): a link that the user has attached to the post
			content(str): the content the user has provided in the post
			created_at(str): the date/time that the user had created the post
			likes(int): the amount of likes the post has
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM POSTS WHERE forum_name = ? ORDER BY created_at"""
	cursor.execute(query, [name])
	result = cursor.fetchall()
	con.close()
	return result

def check_post_exists(post_id):
	'''Checks if the post exists in case a user tries to directly use the URL
	to make a comment on the post or like the post
	Arguments:
		post_id(int): the unique identifier of the post the user is trying to comment/like
	Returns:
		True if the post exists in the database, False otherwise
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM POSTS WHERE post_id = ?"""
	cursor.execute(query, [post_id])
	result = cursor.fetchall()
	con.close()
	if len(result) == 0:
		return False
	else:
		return True

def remove_post(post_id):
	'''Deletes a post from the database.
	Arguments:
		post_id(int): the id of the post the user is trying to delete
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """DELETE FROM REPLIES WHERE post_id = ?"""
	cursor.execute(query, [post_id])
	con.commit()
	query = """DELETE FROM POSTS WHERE post_id = ?"""
	cursor.execute(query, [post_id])
	con.commit()
	con.close()

def get_author_of_post(post_id):
	'''Gets the userid of the user who created the post that the user is
	trying to delete so only the person that created it can delete it.
	Arguments:
		post_id(int): the id of the post the user is trying to delete
	Returns:
		result(list of tuples): will only contain the userid of a single record
			user_id(int): the userid of the user who created the post
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT user_id FROM POSTS WHERE post_id = ?"""
	cursor.execute(query, [post_id])
	result = cursor.fetchall()
	cursor.close()
	return result

#Database functions for comments and replies

def get_comments():
	'''Gets all the comments(all the replies that are direct replies to the
	post and not a reply to a comment).
	Arguments:
		Nothing
	Returns:
		result(list of tuples): all the comments made on the application
			reply_id(int): the unique identifier of the comment
			user_id(int): the userid of the user who made the comment
			username(str): the username of the user who made the comment
			post_id(int): the id of the post the user made the comment on
			content(str): the comment the user made
			created_at(str): the date/time the user made the comment
			likes(int): the amount of the likes the amount has
			reply_parent_id(int): set to NULL as it is not a reply
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM REPLIES WHERE reply_parent_id IS NULL"""
	cursor.execute(query)
	result = cursor.fetchall()
	con.close()
	return result

def get_replies():
	'''Gets all the replies (anything in the replies table that has a
	reply_parent_id)
	Arguments:
		Nothing
	Returns:
		result(list of tuples): all the replies made on the application
			reply_id(int): the unique identifier of the reply
			user_id(int): the userid of the user who made the reply
			username(str): the username of the user who made the reply
			post_id(int): the id of the post the user made the reply on
			content(str): the reply the user made
			created_at(str): the date/time the user made the reply
			likes(int): the amount of the likes the amount has
			reply_parent_id(int): the id of the comment the reply was made to
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM REPLIES"""
	cursor.execute(query)
	result = cursor.fetchall()
	con.close()
	return result

def add_comment_or_reply(content, user_id, username, post_id, reply_parent_id, date):
	'''Adds the comment/reply the user has made into the database.
	Arguments:
		content(str): the comment/reply the user has made
		user_id(int): the userid of the user currently logged in
		username(str): the username of the user who made the comment/reply
		post_id(int): the id of the post the user is making the comment/reply on
		reply_parent_id(int): NULL if a comment, if a reply, the comment id that
		the user is replying to
		date(str): the current date/time the user is making the comment/reply
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO REPLIES (user_id, username, post_id, content, created_at, likes, reply_parent_id) VALUES(?,?,?,?,?,?,?) """
	cursor.execute(query, [user_id, username, post_id, content, date, 0, reply_parent_id])
	con.commit()
	con.close()

def check_comment_exists(comment_id):
	'''Checks if the comment the user is replying to or trying to like exists in the
	database in case they use the URL to directly perform these actions.
	Arguments:
		comment_id(int): the id of the comment the user is trying to reply to or like
	Returns:
		True if the comment exists, False otherwise
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM REPLIES WHERE reply_id = ?"""
	cursor.execute(query, [comment_id])
	result = cursor.fetchall()
	con.close()
	if len(result) == 0:
		return False
	else:
		return True

def get_author_of_comment(comment_id):
	'''Gets the user id of the user who created the comment that the user is trying
	to delete so only the user who created it can delete it.
	Arguments:
		comment_id(int): the id of the comment the user is trying to delete
	Returns:
		result(list of tuples): will only contain the userid of a single record
			user_id(int): the userid of the user who created the comment/reply
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT user_id FROM REPLIES WHERE reply_id = ?"""
	cursor.execute(query, [comment_id])
	result = cursor.fetchall()
	cursor.close()
	return result

def remove_comment(reply_id):
	'''Deletes a comment/reply from the database.
	Arguments:
		reply_id(int): the id of the comment/reply the user is trying to delete
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """ DELETE FROM REPLIES WHERE reply_id = ?"""
	cursor.execute(query, [reply_id])
	con.commit()
	con.close()

def remove_replies(reply_id):
	'''Delets all replies to a comment from the database.
	Arguments:
		reply_id(int): the id of the comment that has been deleted
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """DELETE FROM REPLIES WHERE reply_parent_id = ?"""
	cursor.execute(query, [reply_id])
	con.commit()
	con.close()

#Database functions for likes

def add_like_post(user_id, post_id):
	'''Adds a record to the database to show that the user has liked a 
	post and increments the amount of likes of the post by 1.
	Arguemnts:
		user_id(int): the userid of the user currently logged in
		post_id(int): the id of the post that the user has liked
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO LIKES_POST(user_id,post_id) VALUES (?,?)"""
	cursor.execute(query, [user_id, post_id])
	con.commit()
	query = """ UPDATE POSTS SET likes = likes + 1 WHERE post_id = ?"""
	cursor.execute(query, [post_id])
	con.commit()
	con.close()

def add_like_reply(user_id, reply_id):
	'''Adds a record to the database to show that the user has liked a 
	comment/reply and increments the amount of likes of the comment/reply 
	by 1.
	Arguemnts:
		user_id(int): the userid of the user currently logged in
		reply_id(int): the id of the comment/reply that the user has liked
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO LIKES_REPLY(user_id, reply_id) VALUES (?,?)"""
	cursor.execute(query, [user_id, reply_id])
	con.commit()
	query = """UPDATE REPLIES SET likes = likes + 1 WHERE reply_id = ?"""
	cursor.execute(query, [reply_id])
	con.commit()
	con.close()

def check_like_post(user_id, post_id):
	'''Checks that the user has already liked a specific post so they cannot spam
	like the post
	Arguments:
		user_id(int): the userid of the user currently logged in
		post_id(int): the id of the post that the user is trying to like
	Returns:
		True if the user has already liked the post, False otherwise
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM LIKES_POST WHERE user_id = ? AND post_id = ?"""
	cursor.execute(query, [user_id, post_id])
	result = cursor.fetchall()
	con.close()
	if len(result) == 0:
		return False
	else:
		return True

def check_like_reply(user_id, reply_id):
	'''Checks that the user has already liked a specific comment/reply so they
	cannot spam like the comment/reply.
	Arguments:
		user_id(int): the userid of the user currently logged in
		reply_id(int): the id of the comment/reply that the user is trying to like
	Returns:
		True if the user has already liked the comment/reply, False otherwise
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM LIKES_REPLY WHERE user_id = ? AND reply_id = ?"""
	cursor.execute(query, [user_id, reply_id])
	result = cursor.fetchall()
	con.close()
	if len(result) == 0:
		return False
	else:
		return True

def remove_like_post(user_id, post_id):
	'''Deletes the record that the user has liked the post and decrements the
	amount of likes on the post by 1.
	Arguments:
		user_id(int): the userid of the user currently logged in
		post_id(int): the id of the post that the user is trying to unlike
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """DELETE FROM LIKES_POST WHERE user_id = ? AND post_id = ?"""
	cursor.execute(query, [user_id, post_id])
	con.commit()
	query = """UPDATE POSTS SET likes = likes - 1 WHERE post_id = ?"""
	cursor.execute(query, [post_id])
	con.commit()
	con.close()

def remove_like_reply(user_id, reply_id):
	'''Deletes the record that the user has liked the comment/reply and decrements 
	the amount of likes on the comment/reply by 1.
	Arguments:
		user_id(int): the userid of the user currently logged in
		reply_id(int): the id of the comment/reply the user is trying to unlike
	Returns:
		Nothing
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """DELETE FROM LIKES_REPLY WHERE user_id = ? AND reply_id = ?"""
	cursor.execute(query, [user_id, reply_id])
	con.commit()
	query = """UPDATE REPLIES SET likes = likes - 1 WHERE reply_id = ?"""
	cursor.execute(query, [reply_id])
	con.commit()
	con.close()
	
def get_user_email(user_id):
    '''
    Retrieves the email of a specific user from the database
    Arguments:
        user_id(int): user_id of the provided user
    Returns:
        result(list of tuples) will only have one email:
            email(str): the users provided email address
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = "SELECT email FROM USER WHERE user_id = ?"""
    cursor.execute(query, [user_id])
    result = cursor.fetchall()
    con.close()
    return result


def replace_user_email(user_id, email):
    '''
    Replaces the users email with one they have provided in the database
    Arguments:
        user_id(int): the user_id of the user replacing their email
        email(str): the email provided to replace the previously entered one
    Returns:
        Null
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """UPDATE USER SET email =  ? WHERE user_id = ?"""
    cursor.execute(query, [email, user_id])
    con.commit()
    con.close()

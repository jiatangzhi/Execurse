import hashing
import database_functions as db
import verification_code
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash, abort
import ChallengesQuiz as game
import random

app = Flask(__name__)
app.secret_key = "secret"

global verification_first,verification_wrong_code,verification_email_sent,verification_resend
verification_email_sent = False #used in verification
verification_wrong_code = False #used in verification
verification_resend = False #used in verification
verification_first = True

@app.route('/', methods=["POST", "GET"])
def login():
	'''The login page for the application.
	Arguments:
		Nothing
	Returns:
		redirect(url_for("forum")): redirects user to forum page on successful login
		render_template("login.html"): gets the login.html file from the templates folder
		redirect(url_for("forum")): redirects user to forum page if they are already logged in
	'''
	if "username" not in session: #Checks if the user is not logged in
		
		if request.method == "POST": #When the form is submitted
			username = request.form["username"] #Gets data from the username field 
			password = request.form["password"] #Gets data from the password field
			
			if username == '': #Checks if the string is empty
				flash("Username not entered") #Flashes a message on the webpage
			
			elif db.check_username_already_used(username) == False:
				flash("User does not exist")
			
			else:
				
				database_password = db.get_password_hash(username)
				
				if hashing.check_password(username, password, database_password) == False:
					flash("Incorrect Password")
				
				else:
					#Adds new variables to the session dictionary to signify the user being logged in
					session["userid"] = db.get_user_id(username)
					session["username"] = username
					session["account"] = db.get_user_type(username)
					if game.check_username_already_used_in_table("DAILYCHALLENGES", username) == False:
						game.initiate_challenge_at_database(username)
					game.challenge_points_assignment_function(username, "login")
					game.table_reset_function()
					return redirect(url_for("forum"))
		
		return render_template("login.html")
	
	else:
		return redirect(url_for("forum"))

@app.route('/signup', methods=["POST", "GET"])
def signup():
	'''The signup page for the application.
	Arguments:
		Nothing
	Returns:
		redirect(url_for("account_verification")): redirects user to the verification page on successful signup
		render_template("signup.html"): gets the signup.html file from the templates folder
	'''
	global verification_username
	if request.method == "POST":
		
		username = request.form["username"]
		password = request.form["password"]
		confirm = request.form["confirm"]
		email = request.form["email"]

		error = False
		
		if username == '':
			flash("Please enter a username", "username_error")
			error = True
		elif len(username) < 4: #if length of username is less than 4
			flash("Username must be at least 4 characters", "username_error")
			#Categorizes the messsage into a category called "username_error"
			error = True
		elif len(username) > 25: #if length of username is greater than 25
			flash("Username must not exceed 25 characters", "username_error")
			error = True
		elif " " in username: #if the username contains any whitespaces
			flash("Username must not contain any spaces", "username_error")
			error = True
		elif db.check_username_already_used(username) == True:
			flash("Username is already being used", "username_error")
			error = True

		if password == '':
			flash("Please enter a password", "password_error")
			error = True
		elif len(password) < 8:
			flash("Password must be at least 8 characters long", "password_error")
			error = True
		elif not any(char.isupper() for char in password): #if the password contains no uppercase letters
			flash("Password must contain at least 1 uppercase letter", "password_error")
			error = True
		elif not any(char.islower() for char in password): #if the password contans no lowercase letters
			flash("Password must contain at least 1 lowercase letter", "password_error")
			error = True
		elif not any(char.isdigit() for char in password): #if the password contains no numbers
			flash("Password must contain at least 1 number", "password_error")
			error = True
		elif confirm != password: #if the password does not match the other password the user entered
			flash("Passwords do not match", "password_error")
			error = True
		
		if email == '':
			flash("Please enter an email address", "email_error")
			error = True
		elif db.check_email_already_used(email) == True:
			flash("Email is already registed to an account", "email_error")
			error = True

		if error == False:
			hashed_password = hashing.hash_password(username, password)
			db.add_user(username, hashed_password, email, 0)
			session["verificationusername"] = username
			return redirect(url_for("account_verification"))

	return render_template("signup.html")


@app.route("/verification")
def account_verification():
    '''the verification page for the application
    Arguements:
        Nothing
    Returns:
        redirect(url_for("login"))): redirect user to login if code entered correctly
        verify_account: html for the page
    '''
    import send_email
    global verification_first,verification_wrong_code,verification_email_sent,verification_resend
    exists = False
    if verification_first == True:
        session["verificationcode"] = verification_code.create_code() #used in verification
        verification_first = False

    entered_code = request.args.get("entered_code")
    verification_resend = request.args.get("resend_email")
    update = request.args.get("update_email")
    
    if entered_code:
        if entered_code == session["verificationcode"]:
            verification_username = ""
            verification_first = True
            return (redirect(url_for("login")))
        else:
            verification_wrong_code = True
            
    if verification_resend == "":
        verification_email_sent = False
        verification_resend = False
        
    if update:
        if db.check_email_already_used(update) == True:
            exists = True
        else:
            user = session["verificationusername"]
            user_id = db.get_user_id(user)
            db.replace_user_email(user_id,update)
            verification_email_sent = False

    if verification_email_sent == False:
        user = session["verificationusername"]
        user_id = db.get_user_id(user)
        user_email = db.get_user_email(user_id)
        send_email.send_code(user_email,session["verificationcode"])
        verification_email_sent = True


    verify_account = """to verify your account, we have sent a code to your email<br>\
    please enter that code in the box below<br>\
    <form action = '/verification' method = 'get'>\
    <input type = 'text' name = 'entered_code'></form>"""
    if verification_wrong_code == True:
        verify_account = verify_account + """\
        that was not the correct code. please try again"""
    verify_account = verify_account + """<br>\
    <form action = '/verification' method = 'get'>\
    <button type = 'submit' name = 'resend_email'>Resend Email</button></form>"""
    verify_account = verify_account + """<br><br>\
    want to change your email address? do so in the box below<br>"""
    verify_account = verify_account + """\
    <form action = '/verification' method = 'get'>\
    <input type = 'text' name = 'update_email'></form>"""
    if exists == True:
        verify_account = verify_account + "<br> email already in use, please enter another one"

    return verify_account


@app.route('/forum', methods=["POST", "GET"])
def forum():
	'''The forum page for the application.
	Arguments:
		Nothing
	Returns:
		render_template("forum.html", subforums=subforums): gets the forum.html file from the templates folder
			Parameters:
				subforums(list of tuples): all the subforums on the application
		redirect(url_for("login")): redirects user back to the login page if they are not logged in
	'''
	if "username" in session: #Checks if the user is logged in

		if request.method == "POST":

			subforum = request.form["subforum"].lower()

			if subforum == "":
				flash("Please submit a name for a new subforum")
			elif db.check_duplicate_forum(subforum) == True:
				flash("There already exists a subforum with that name")
			else:
				db.create_new_forum(subforum)

		subforums = db.get_all_forums()		

		return render_template("forum.html", subforums=subforums)
	
	else:
		return redirect(url_for("login"))

@app.route('/remove_subforum/<name>', methods=["POST", "GET"])
def remove_subforum(name):
	'''Removes a subforum from the application.
	Arguments:
		name(str): the name of the subforum that the user wants to delete
	Returns:
		redirect(url_for("forum")): redirects user back to the forum after the action is complete
		redirect(url_for("login")): redirects user back to the login page if they are not logged in
	Errors:
		400: when the user is trying to delete a subforum that does not exist
		403: when the user trying to delete a subforum is not an academic user
	'''
	if "username" in session:
		
		if session["account"] == 1:
			
			if db.check_duplicate_forum(name) == True:
				db.delete_forum(name)
				return redirect(url_for("forum"))
			
			else:
				abort(400)
		else:
			abort(403)
	
	else:
		return redirect(url_for("login"))

@app.route('/forum/<name>')
def subforum(name):
	'''Every subforum page for the application.
	Arguments:
		name(str): the name of the subforum that the user is currently on
	Returns:
		render_template("subforum.html", name=name, posts=posts, comments=comments, replies=replies):
		gets the subforum.html file from the templates folder
			Parameters:
				name(str): the name of the subforum that the user is currently on
				posts(list of tuples): all the posts on the subforum
				comments(list of tuples): all the comments made on the application
				replies(list of tuples): all the replies made on the application
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		404: when the user tries to go to a subforum that does not exist
	'''
	if "username" in session:
		
		if db.check_duplicate_forum(name) == True:
			posts = db.get_posts(name)
			comments = db.get_comments()
			replies = db.get_replies()
			return render_template("subforum.html", name=name, posts=posts, comments=comments, replies=replies)
		
		else:
			abort(404)
	
	else:
		return redirect(url_for("login"))

@app.route('/add_comment/<name>/<post_id>', methods=["POST", "GET"])
def add_comment(post_id, name):
	'''Adds a new comment to a post on the application.
	Arguments:
		post_id(int): the id of the post the user is commenting on
		name(str): the name of the subforum the user is currently on
	Returns:
		redirect(url_for("subforum", name=name)): redirects the user back to the subforum they
		were on after the comment has been added
			Parameters:
				name(str): the name of the subforum
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		400: when the user tries to comment on a post that does not exist
	'''
	if "username" in session:

		if db.check_post_exists(post_id) == True:
			
			comment = request.form["comment"]
			
			if comment != "":
				userid = session["userid"]
				username = session["username"]
				date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
				db.add_comment_or_reply(comment, userid, username, post_id, None, date)
				game.challenge_points_assignment_function(username, "add_comments")
				return redirect(url_for("subforum", name=name))

		else:
			abort(400)

	else:
		return redirect(url_for("login"))

@app.route('/reply_comment/<name>/<post_id>/<comment_id>', methods=["POST", "GET"])
def reply_comment(comment_id, post_id, name):
	'''Adds a new reply to a comment on the application.
	Arguments:
		comment_id(int): the id of the comment the user is replying to
		post_id(int): the id of the post the comment is on
		name(str): the name of the subforum the user is currently on
	Returns:
		redirect(url_for("subforum", name=name)): redirects the user back to the subforum they
		were on after the reply has been added
			Parameters:
				name(str): the name of the subforum
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		400: when the user is trying to reply to a comment that does not exist
	'''
	if "username" in session:

		if db.check_comment_exists(comment_id) == True:
			
			reply = request.form["reply"]
			
			if reply != "":
				userid = session["userid"]
				username = session["username"]
				date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
				db.add_comment_or_reply(reply, userid, username, post_id, comment_id, date)
				game.challenge_points_assignment_function(username, "reply_comments")
				return redirect(url_for("subforum", name=name))

		else:
			abort(400)

	else:
		return redirect(url_for("login"))

@app.route('/like_comment/<name>/<comment_id>', methods=["POST", "GET"])
def like_comment(comment_id, name):
	'''Likes a comment/reply on the application.
	Arguments:
		comment_id(int): the id of the comment/reply the user is liking
		name(str): the name of the subforum the user is currently on
	Returns:
		redirect(url_for("subforum", name=name)): redirects the user back to the subforum they
		were on after the comment/reply has been liked
			Parameters:
				name(str): the name of the subforum
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		400: when the user likes a comment/reply that does not exist
	'''
	if "username" in session:

		if db.check_comment_exists(comment_id) == True:

			userid = session["userid"]
			user_name = session["username"]

			if db.check_like_reply(userid, comment_id) == False:
				db.add_like_reply(userid, comment_id)
				game.challenge_points_assignment_function(user_name, "like_comments")

			else:
				db.remove_like_reply(userid, comment_id)

			return redirect(url_for("subforum", name=name))

		else:
			abort(400)

	else:
		return redirect(url_for("login"))

@app.route('/remove_comment/<name>/<comment_id>', methods=["POST", "GET"])
def remove_comment(comment_id, name):
	'''Removes a comment/reply on the application.
	Arguments:
		comment_id(int): the id of the comment/reply the user is trying to remove
		name(str): the name of the subforum the user is currently on
	Returns:
		redirect(url_for("subforum", name=name)): redirects the user back to the subforum they
		were on after the comment/reply has been removed
			Parameters:
				name(str): the name of the subforum
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		400: when the user tries to remove a comment/reply that does not exist
		403: when the user deleting the comment/reply is not the author or an academic user
	'''
	if "username" in session:

		user = db.get_author_of_comment(comment_id)
		
		if len(user) != 0:
			
			if session["account"] == 1 or session["userid"] == user[0][0]:
				db.remove_comment(comment_id)
				db.remove_replies(comment_id)
				return redirect(url_for("subforum", name=name))
			
			else:
				abort(403)
		
		else:
			abort(400)

	else:
		return redirect(url_for("login"))

@app.route('/forum/<name>/add_new_post', methods=["POST", "GET"])
def add_new_post(name):
	'''The add post page for the application
	Arguments:
		name(str): the name of the subforum the user is currently on
	Returns:
		redirect(url_for("subforum", name=name)): redirects the user back to the subforum once
		they have successfully created a new post on that subforum
			Parameters:
				name(str): the name of the subforum
		render_template("addNewPost.html", name=name): gets the addNewPost.html file from the templates
		folder
			Parameters:
				name(str): the name of the subforum
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		404: when the user tries to add a post to a subforum that does not exist
	'''
	if "username" in session:

		if db.check_duplicate_forum(name) == True:

			userid = session["userid"]
			username = session["username"]

			if request.method == "POST":

				title = request.form["title"]
				link = request.form["link"]
				description = request.form["description"]

				error = False

				if title == '':
					flash("Please make a title for this post", "title_error")
					error = True

				if len(description) == 0:
					flash("Please provide a description for this post", "description_error")
					error = True
				elif len(description) > 300:
					flash("Maximum amount of characters exceeded", "description_error")
					error = True

				if error == False:
					date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
					db.add_post(userid, username, name, title, link, description, date, 0)
					game.challenge_points_assignment_function(username, "add_posts")
					return redirect(url_for("subforum", name=name))

			return render_template("addNewPost.html", name=name)

		else:
			
			abort(404)
		
	else:
		return redirect(url_for("login"))

@app.route('/like_post/<name>/<post_id>', methods=["POST", "GET"])
def like_post(post_id, name):
	'''Likes a post on the application.
	Arguments:
		post_id(int): the id of the post the user is liking
		name(str): the name of the subforum the user is currently on
	Returns:
		redirect(url_for("subforum", name=name)): redirects the user back to the subforum they
		were on after the post has been liked
			Parameters:
				name(str): the name of the subforum
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		400: when the user likes a post that does not exist
	'''
	if "username" in session:

		if db.check_post_exists(post_id) == True:

			userid = session["userid"]
			user_name = session["username"]

			if db.check_like_post(userid, post_id) == False:
				db.add_like_post(userid, post_id)
				game.challenge_points_assignment_function(user_name, "like_posts")

			else:
				db.remove_like_post(userid, post_id)

			return redirect(url_for("subforum", name=name))

		else:
			abort(400)

	else:
		return redirect(url_for("login"))

@app.route('/remove_post/<name>/<post_id>', methods=["POST", "GET"])
def remove_post(post_id, name):
	'''Removes a post on the application.
	Arguments:
		comment_id(int): the id of the post the user is trying to remove
		name(str): the name of the subforum the user is currently on
	Returns:
		redirect(url_for("subforum", name=name)): redirects the user back to the subforum they
		were on after the post has been removed
			Parameters:
				name(str): the name of the subforum
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		400: when the user tries to remove a post that does not exist
		403: when the user deleting the post is not the author or an academic user
	'''
	if "username" in session:
		
		user = db.get_author_of_post(post_id)
		
		if len(user) != 0:
			
			if session["account"] == 1 or session["userid"] == user[0][0]:
				db.remove_post(post_id)
				return redirect(url_for("subforum", name=name))
			
			else:
				abort(403)
		
		else:
			abort(400)

	else:
		return redirect(url_for("login"))

@app.route('/support_network', methods=["POST", "GET"])
def support_network():
	'''The support network page for the application
	Arguments:
		Nothing
	Return:
		render_template("supportNetwork.html", network=network): gets the supportNetwork.html file
		from the templates folder
			Parameters:
				network(list of tuples): All the people in the user's support network
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	'''
	if "username" in session:
		
		userid = session["userid"]

		if request.method == "POST":
			email = request.form["email"]
			firstname = request.form["firstname"]
			lastname = request.form["lastname"]
			relation = request.form["relation"]
			other = request.form["other"]

			error = False

			if email == '':
				flash("Please enter an email address", "email_error")
				error = True
			elif len(db.check_support_network(userid, email)) > 0:
				flash("Email is already registered on support_network", "email_error")
				error = True

			if firstname == '':
				flash("Please enter their first name", "name_error")
				error = True
			elif lastname == '':
				flash("Please enter their last name", "name_error")
				error = True
			elif firstname.isalpha() == False:
				flash("First name should only contain letters", "name_error")
				error = True
			elif lastname.isalpha() == False:
				flash("Last name should only contain letters", "name_error")
				error = True

			if relation == "Other":
				if other == "":
					flash("Please fill out the box", "relation_error")
					error = True

			if error == False:
				if relation == "Other":
					db.add_to_support_network(userid, email, firstname, lastname, other)
				else:
					db.add_to_support_network(userid, email, firstname, lastname, relation)

		network = db.get_support_network(userid)
		return render_template("supportNetwork.html", network=network)
	
	else:
		return redirect(url_for("login"))

@app.route('/remove_email/<email_id>', methods=["POST", "GET"])
def remove_email(email_id):
	'''Removes an email from the user's support network on the application.
	Arguments:
		email_id(int): the id of the email the user is trying to remove
	Returns:
		redirect(url_for("support_network")): redirect the user back to the support network page after the
		email has been removed from the application
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	Errors:
		400: when the user tries to remove a email that does not exist
		403: when the user deleting the email is not the user who registered it
	'''
	if "username" in session:
		user = db.get_userid_email(email_id)
		
		if len(user) != 0:
			
			if session["userid"] == user[0][0]:
				db.delete_from_support_network(email_id)
				return redirect(url_for("support_network"))
			
			else:
				abort(403)

		else:
			abort(400)

	else:
		return redirect(url_for("login"))

@app.route('/leaderboard', methods=["POST", "GET"])
def leaderboard():
	'''The leaderboard page for the application.
	Arguments:
		Nothing
	Returns:
		render_template("leaderboard.html", scores=scores): gets the leaderboard.html file from the 
		templates folder
			Parameters:
				scores(list of tuples): the leaderboard information
		redirect(url_for("login.html")): redirects user back to the login page if they are not logged in
	'''
	if "username" in session:
		game.table_reset_function()
		scores = db.get_scores()
		scores2 = db.get_scores_for_weekly_table()
		return render_template("leaderboard.html", all_time=scores, weekly=scores2)

	else:
		return redirect(url_for("login"))

@app.route('/logout')
def logout():
	'''Logs the user out of the application
	Arguments:
		Nothing
	Returns:
		redirect(url_for("login.html")): redirects user back to the login page when they log out
	'''
	if "username" in session:
		session.pop("username")
		session.pop("userid")
		session.pop("account")

	return redirect(url_for("login"))

@app.route("/settings", methods=["POST", "GET"])
def settings():
	if "username" in session:
		#freedom of editing your personal preferences
		# pass word and e-mail
		user_id = session["userid"]
		user_name= session["username"]
		e_mail = db.get_user_eemail(user_id)
		if request.method == "POST":
			new_name = request.form["u_name"]
			new_password = request.form["password"]
			confirm = request.form["password2"]
			new_mail = request.form["e_mail"]

			edit_successful= False
			error = False

			if user_name != new_name:
				if new_name == '':
					flash("Please enter a username", "username_error")
					error = True
				elif len(new_name) < 4:  # if length of username is less than 4
					flash("Username must be at least 4 characters", "username_error")
					# Categorizes the messsage into a category called "username_error"
					error = True
				elif len(new_name) > 25:  # if length of username is greater than 25
					flash("Username must not exceed 25 characters", "username_error")
					error = True
				elif " " in new_name:  # if the username contains any whitespaces
					flash("Username must not contain any spaces", "username_error")
					error = True
				elif db.check_username_already_used(new_name) == True:
					flash("Username is already being used", "username_error")
					error = True

			if new_password != '':
				if len(new_password) < 8:
					flash("Password must be at least 8 characters long", "password_error")
					error = True
				elif not any(char.isupper() for char in new_password):  # if the password contains no uppercase letters
					flash("Password must contain at least 1 uppercase letter", "password_error")
					error = True
				elif not any(char.islower() for char in new_password):  # if the password contans no lowercase letters
					flash("Password must contain at least 1 lowercase letter", "password_error")
					error = True
				elif not any(char.isdigit() for char in new_password):  # if the password contains no numbers
					flash("Password must contain at least 1 number", "password_error")
					error = True
				elif confirm != new_password:  # if the password does not match the other password the user entered
					flash("Passwords do not match", "password_error")
					error = True

			if new_mail != e_mail:
				if new_mail == '':
					flash("Please enter an email address", "email_error")
					error = True
				elif db.check_email_already_used(new_mail) == True:
					flash("Email is already registed to an account", "email_error")
					error = True

			if error == False:
				if user_name != new_name:
					db.edit_personal_data(user_id,'username',new_name)
					edit_successful=True
				if new_password != '':

					get_name= db.get_user_name_from_id(user_id)
					hashed_password = hashing.hash_password(get_name, new_password)
					db.edit_personal_data(user_id,'password',hashed_password)
					edit_successful=True
				if new_mail != e_mail:
					db.edit_personal_data(user_id,'email',new_mail)
					edit_successful=True

			if edit_successful == True:
				# making the user know her/his changes were saved

				done= 'Your Edit Was Successful'
				return redirect(url_for("settings", successful= done))

			return render_template("settings.html", u_name= user_name,e_mail= e_mail)
		else:
			return render_template("settings.html", u_name= user_name,e_mail= e_mail)
	else:

		return redirect(url_for("login"))


@app.route('/dailyChallenges', methods=["POST", "GET"])
def dailyboard():
	''' this page immediately sets the user his/her specific challenge
		also runs functions that check challenge progress
		also runs functions that gives you your full points when challenges are completed
	'''
	if "username" in session:
		user_name = session["username"]
		game.create_daily_challenge(user_name)
		# if challenges are completed
		# if table status is false
		# add the rewards to the WEEKLY AND USER database

		statement = "The rules are simple, complete the challenges to get 30 points today!"
		if game.daily_challenge_status_complete(user_name) == True:
			statement = "Congratulations!!!. You Have earned your daily points(30!), See you tomorrow."
			if game.daily_challenge_status_check(user_name) == False:
				game.points_adding_function_user_name("USER", user_name, 30)
				game.points_adding_function_user_name("WEEKLYBOARD", user_name, 30)
				game.set_challenge_done(user_name)

		objectives = [["login", "like_comments", "reply_comments"], ["add_posts", "like_posts", "add_comments"]]
		c_type = game.get_challenge_type(user_name)
		challenges = objectives[c_type]

		scores = game.get_daily_challenge_table(user_name)  # Gets all the user scores from the database

		return render_template("dailyChallenges.html", scores=scores, tasks=challenges, status=statement)

	else:
		return redirect(url_for("login"))


@app.route('/dailyQuiz', methods=["POST", "GET"])
def dailyQandA():
	'''
	runs neccessary functions to make assemble the users Quiz.
	In an orderly manner
	all functions here are throughly described in ChallengesQUiz.py
	:return: either a challenge or no challenge that reminds the user of the process and his/her past scores
	'''
	if "username" in session:

		user_name = session["username"]

		if request.method == "POST":
			game.the_quiz_has_been_taken(user_name)
			users_work = [request.form['Q1'], request.form['Q2'], request.form['Q3']]
			the_answer = [request.form['A1'], request.form['A2'], request.form['A3']]
			score = game.results_and_processing(users_work, the_answer)
			game.points_adding_function_user_name("USER", user_name, score)
			game.points_adding_function_user_name("WEEKLYBOARD", user_name, score)
			game.points_adding_function_user_name("DAILYQUIZ", user_name, score)

			statement = "nice try, you scored " + str(score) + " points. See you tomorrow!!!"
			if score == 0:
				statement = "You scored 0 looser!, Come back tomorrow. Maybe you wont be"
			elif score == 30:
				statement = "You scored 15 points!. You also get  X2 multiplier for a perfect record"
			return render_template("dailyQuiz.html", quiz=[], answer="", quiz_taken=statement)

		# if youre not in the database, then you should be immediately inserted
		if game.check_username_already_used_in_table("DAILYQUIZ", user_name) == False:
			game.create_daily_quiz_instance(user_name)
		#if you havent done your previous challenges but its a new day, you canplay
		if game.quiz_status_verifier(user_name) == False:
			if game.date_verification_for_existing_challenger("DAILYQUIZ", user_name, "daily") == True:
				game.update_quiz_instance(user_name)
				the_quiz = random.sample(game.question_prompts, 3)
				the_answer = [the_quiz[0][5], the_quiz[1][5], the_quiz[2][5]]
				return render_template("dailyQuiz.html", quiz=the_quiz, answer=the_answer, quiz_taken="")
			
		if game.quiz_status_verifier(user_name) == True:
			if game.date_verification_for_existing_challenger("DAILYQUIZ", user_name, "daily") == True:
				game.update_quiz_instance(user_name)
				the_quiz = random.sample(game.question_prompts, 3)
				the_answer = [the_quiz[0][5], the_quiz[1][5], the_quiz[2][5]]
				return render_template("dailyQuiz.html", quiz=the_quiz, answer=the_answer, quiz_taken="")
		# key: if you havent done you challenges and you still have some time left, you can proceed
		if game.quiz_status_verifier(user_name) == False:
			the_quiz = random.sample(game.question_prompts, 3)
			the_answer = [the_quiz[0][5], the_quiz[1][5], the_quiz[2][5]]
			return render_template("dailyQuiz.html", quiz=the_quiz, answer=the_answer, quiz_taken="")
		
		if game.quiz_status_verifier(user_name) == True:
			score = game.get_user_score("DAILYQUIZ", user_name)
			see_you_tomorrow = "You have already played, you scored "+ str(score) + " points. See you tomorrow!!!"
			return render_template("dailyQuiz.html", quiz=[], answer="", quiz_taken=see_you_tomorrow)

		return render_template("dailyQuiz.html", quiz=[], answer="", quiz_taken="")
	else:
		return redirect(url_for("login"))


@app.errorhandler(400)
def error400(error):
	'''When a 400 error in the application is raised
	Arguments:
		error(int): the error code
	Returns:
		render_template("400.html"): gets the 400.html file from the templates folder
	'''
	return render_template("400.html")

@app.errorhandler(403)
def error403(error):
	'''When a 403 error in the application is raised
	Arguments:
		error(int): the error code
	Returns:
		render_template("403.html"): gets the 400.html file from the templates folder
	'''
	return render_template("403.html")

@app.errorhandler(404)
def error404(error):
	'''When a 404 error in the application is raised
	Arguments:
		error(int): the error code
	Returns:
		render_template("404.html"): gets the 404.html file from the templates folder
	'''
	return render_template("404.html")

@app.errorhandler(500)
def error500(error):
	'''When a 500 error in the application is raised
	Arguments:
		error(int): the error code
	Returns:
		render_template("500.html"): gets the 500.html file from the templates folder
	'''
	return render_template("500.html")

f = open("Host Port.txt", "r")
portNum = int(str(f.readline())[12:])
f.close()

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=portNum)

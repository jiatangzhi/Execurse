import hashing
import database_functions as db
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = "secret" #Secret key to prevent cross-site script attacks (should be environmental variable)

@app.route('/', methods=["POST", "GET"])
def login():
	
	if "username" not in session: #Checks if the user is not in a session
		
		if request.method == "POST": #If the user submits the form
			username = request.form["username"] #Get the username from the username field
			password = request.form["password"] #Get the password from the password field
			
			#Validation for the username
			if username == '':
				flash("Username not entered")
			elif db.check_username_already_used(username) == False:
				flash("User does not exist")
			else:
				#Validation for the password
				database_password = db.get_password_hash(username) #Gets the password has from the database
				
				if hashing.check_password(username, password, database_password) == False:
					flash("Incorrect Password")
				else:
					#Adds the user details as session variables to be accessed on other pages
					session["userid"] = db.get_user_id(username)
					session["username"] = username
					session["account"] = db.get_user_type(username)
					return redirect(url_for("forum"))
		
		return render_template("login.html") #Gets the login page from the templates
	
	else:
		return redirect(url_for("forum")) #Redirects the user in the forum if the user is already logged in

@app.route('/signup', methods=["POST", "GET"])
def signup():
	
	if request.method == "POST":
		
		username = request.form["username"]
		password = request.form["password"]
		confirm = request.form["confirm"]
		email = request.form["email"]

		error = False
		
		#Validation for the username
		if username == '': #Checks if the field is empty on submission
			flash("Please enter a username", "username_error")
			error = True
		elif len(username) < 4: #Checks the length of the username
			flash("Username must be at least 4 characters", "username_error")
			error = True
		elif len(username) > 25:
			flash("Username must not exceed 25 characters", "username_error")
			error = True
		elif " " in username: #Checks if there are any whitespaces in the username
			flash("Username must not contain any spaces", "username_error")
			error = True
		elif db.check_username_already_used(username) == True:
			flash("Username is already being used", "username_error")
			error = True

		#Validation for the password
		if password == '':
			flash("Please enter a password", "password_error")
			error = True
		elif len(password) < 8:
			flash("Password must be at least 8 characters long", "password_error")
			error = True
		elif not any(char.isupper() for char in password): #Checks if there is an uppercase letter
			flash("Password must contain at least 1 uppercase letter", "password_error")
			error = True
		elif not any(char.islower() for char in password): #Checks if there is a lowercase letter
			flash("Password must contain at least 1 lowercase letter", "password_error")
			error = True
		elif not any(char.isdigit() for char in password): #Checks if the password contains numbers
			flash("Password must contain at least 1 number", "password_error")
			error = True
		elif confirm != password: #Compares the passwords to see if they match
			flash("Passwords do not match", "password_error")
			error = True
		
		#Validation for the email address
		if email == '':
			flash("Please enter an email address", "email_error")
			error = True
		elif db.check_email_already_used(email) == True:
			flash("Email is already registed to an account", "email_error")
			error = True

		#Checks if there was any errors raised in the validation
		if error == False:
			hashed_password = hashing.hash_password(username, password) #Hashes the user's password for added security
			db.add_user(username, hashed_password, email, 0) #Adds the user's account details to the database
			return redirect(url_for("login")) #Redirects them back to the login page

	return render_template("signup.html")


@app.route('/forum')
def forum():
	
	if "username" in session: #Checks if the user is already in a session
		return render_template("forum.html")
	
	else:
		return redirect(url_for("login"))

@app.route('/forum/<name>')
def subforum(name): #arguments: the name of the subforum
	
	if "username" in session:
		posts = db.get_posts(name) #gets all the posts from the database relevant to the current subforum
		return render_template("subforum.html", name=name, posts=posts) #Passes the name of the subforum and the posts to the html page
	
	else:
		return redirect(url_for("login"))

@app.route('/forum/<name>/add_new_post', methods=["POST", "GET"])
def add_new_post(name):
	
	if "username" in session:

		userid = session["userid"] #Sets a variable to an item in session
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
				date = datetime.today().strftime('%d-%m-%Y') #Gets the current date formatted e.g. 24/02/2021
				db.add_post(userid, username, name, title, link, description, date, 0) #Adds a new post to the database
				return redirect(url_for("subforum", name=name)) #Redirects back to the subforum they are currently on

		return render_template("addNewPost.html", name=name)
	
	else:
		return redirect(url_for("login"))

@app.route('/support_network', methods=["POST", "GET"])
def support_network():
	
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
			elif firstname.isalpha() == False: #Checks if the string only consists of letters
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
	db.delete_from_support_network(email_id)
	return redirect(url_for("support_network"))

@app.route('/leaderboard', methods=["POST", "GET"])
def leaderboard():
	scores = db.get_scores() #Gets all the user scores from the database
	return render_template("leaderboard.html", scores=scores)

@app.route('/logout')
def logout(): #When the user clicks the logout button
	if "username" in session: #Checks if the user is logged in
		session.pop("username") #Removes the variable from session
		session.pop("userid")
		session.pop("account")

	return redirect(url_for("login")) #Redirects the user back to the login page

if __name__ == "__main__": #Main function which runs the application
	app.run(debug=True)

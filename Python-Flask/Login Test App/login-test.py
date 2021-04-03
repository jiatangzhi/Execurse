import hashing
import database_functions as db
from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/', methods=["POST", "GET"])
def login():
	if "username" not in session:
		if request.method == "POST":
			username = request.form["username"]
			password = request.form["password"]
			
			if username == '':
				flash("Username not entered")
			elif db.check_username_already_used(username) == False:
				flash("User does not exist")
			else:
				database_password = db.get_password_hash(username)
				
				if hashing.check_password(username, password, database_password) == False:
					flash("Incorrect Password")
				else:
					session["userid"] = db.get_user_id(username)
					session["username"] = username
					session["account"] = db.get_user_type(username)
					return redirect(url_for("forum"))
		
		return render_template("login.html")
	
	else:
		return redirect(url_for("forum"))

@app.route('/signup', methods=["POST", "GET"])
def signup():
	
	if request.method == "POST":
		
		username = request.form["username"]
		password = request.form["password"]
		confirm = request.form["confirm"]
		email = request.form["email"]
		accountType = request.form["accountType"]

		error = False
		
		if username == '':
			flash("Please enter a username", "username_error")
			error = True
		elif len(username) < 4:
			flash("Username must be at least 4 characters", "username_error")
			error = True
		elif len(username) > 25:
			flash("Username must not exceed 25 characters", "username_error")
			error = True
		elif " " in username:
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
		elif not any(char.isupper() for char in password):
			flash("Password must contain at least 1 uppercase letter", "password_error")
			error = True
		elif not any(char.islower() for char in password):
			flash("Password must contain at least 1 lowercase letter", "password_error")
			error = True
		elif not any(char.isdigit() for char in password):
			flash("Password must contain at least 1 number", "password_error")
			error = True
		elif confirm != password:
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
			db.add_user(username, hashed_password, email, accountType)
			return redirect(url_for("login"))

	return render_template("signup.html")


@app.route('/forum')
def forum():
	if "username" in session:
		return render_template("forum.html")
	else:
		return redirect(url_for("login"))

if __name__ == "__main__":
	app.run(debug=True)

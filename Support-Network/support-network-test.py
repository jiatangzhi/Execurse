import sqlite3 as sl
from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "secret"

def get_support_network(userid):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM SUPPORT_EMAILS where user_id = ?"""
	cursor.execute(query, [userid])
	result = cursor.fetchall()
	cursor.close()
	return result

def get_user_id(username):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT user_id FROM USER where username = ?"""
	cursor.execute(query, [username])
	result = cursor.fetchall()
	cursor.close()
	user_id = result[0][0]
	return user_id

def delete_from_support_network(emailid):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """DELETE FROM SUPPORT_EMAILS WHERE email_id = ?"""
	cursor.execute(query, [emailid])
	con.commit()
	cursor.close()

def add_to_support_network(userid, email):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO SUPPORT_EMAILS (user_id, support_email) 
	VALUES (?,?)"""
	cursor.execute(query, [userid, email])
	con.commit()
	cursor.close()

@app.route('/', methods=["POST", "GET"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		userid = get_user_id(username)
		session["userid"] = userid
		session["username"] = username
		return redirect(url_for("support_network"))
	return render_template("login.html")

@app.route('/support_network', methods=["POST", "GET"])
def support_network():
	userid = session["userid"]
	if request.method == "POST":
		email = request.form["email"]
		add_to_support_network(userid, email)

	network = get_support_network(userid)
	return render_template("supportNetwork.html", network=network)

@app.route('/remove_email/<email_id>', methods=["POST"])
def remove_email(email_id):
	delete_from_support_network(email_id)
	return redirect(url_for("support_network"))

if __name__ == "__main__":
	app.run(debug=True)

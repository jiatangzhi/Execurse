import sqlite3 as sl

#Functions for the login and signup pages

def check_username_already_used(username):
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
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO USER (username, password, email, academic)
	VALUES (?, ?, ?, ?)"""
	cursor.execute(query, [username, passwordHash, email, accountType])
	con.commit()
	cursor.close()

def get_password_hash(username):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT password FROM USER where username = ?"""
	cursor.execute(query, [username])
	result = cursor.fetchall()
	cursor.close()
	passwordHash = result[0][0]
	return passwordHash

def get_user_id(username):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT user_id FROM USER where username = ?"""
	cursor.execute(query, [username])
	result = cursor.fetchall()
	cursor.close()
	user_id = result[0][0]
	return user_id

def get_user_type(username):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT academic FROM USER where username = ?"""
	cursor.execute(query, [username])
	result = cursor.fetchall()
	cursor.close()
	accountType = result[0][0]
	return accountType
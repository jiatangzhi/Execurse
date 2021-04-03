import sqlite3 as sl

#Database functions for the login system

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

#Database functions for the support network

def add_to_support_network(userid, email, firstname, lastname, relation):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO SUPPORT_EMAILS (user_id, support_email, firstname, lastname, relation) 
	VALUES (?,?,?,?,?)"""
	cursor.execute(query, [userid, email, firstname, lastname, relation])
	con.commit()
	cursor.close()

def get_support_network(userid):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT * FROM SUPPORT_EMAILS where user_id = ?"""
	cursor.execute(query, [userid])
	result = cursor.fetchall()
	cursor.close()
	return result

def delete_from_support_network(emailid):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """DELETE FROM SUPPORT_EMAILS WHERE email_id = ?"""
	cursor.execute(query, [emailid])
	con.commit()
	cursor.close()

def check_support_network(userid, email):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT support_email FROM SUPPORT_EMAILS WHERE 
	user_id = ? AND support_email = ?"""
	cursor.execute(query, [userid, email])
	result = cursor.fetchall()
	cursor.close()
	return result
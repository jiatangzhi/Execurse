import sqlite3 as sl 

def add_user(username, passwordHash, email, accountType):
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """INSERT INTO USER (username, password, email, academic)
	VALUES (?, ?, ?, ?)"""
	cursor.execute(query, [username, passwordHash, email, accountType])
	con.commit()
	cursor.close()

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


#Just some example code:
if check_username_already_used("example") == True:	
	print("username is already in use")
elif check_email_already_used("example@example.com") == True:
	print("email is already in use")
else:
	add_user("example", "somepasswordhash", "example@example.com", 0)

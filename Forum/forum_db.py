import sqlite3 as sl

def get_all_forums():
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT * FROM FORUMS"""
    cursor.execute(query)
    result = cursor.fetchall()
    con.close()
    return result

def create_new_forum(forum_name):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """INSERT INTO FORUMS (forum_name)
    VALUES(?)"""
    cursor.execute(query, [forum_name])
    con.commit()
    con.close()
    
def delete_forum(forum_name):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM FORUMS WHERE forum_name = ?"""
    cursor.execute(query, [forum_name])
    con.commit()
    con.close()
    
def check_duplicate_forum(forum_name):
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

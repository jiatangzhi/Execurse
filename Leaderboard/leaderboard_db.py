import sqlite3 as sl

#Gets all usernames and the associated scores bigger than 0 and returns them from highest to lowest score
def get_scores():
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT username, current_points FROM USER WHERE current_points > 0 ORDER BY current_points DESC"""
    cursor.execute(query)
    result = cursor.fetchall()
    con.close()
    return result

#Gets a specific users score and returns it
def get_user_score(user_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = "SELECT current_points FROM USER WHERE user_id = ?"""
    cursor.execute(query, [user_id])
    result = cursor.fetchall()
    con.close()
    return result

#Changes a users score and updates the database
def change_user_score(user_id, points):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """UPDATE USER SET current_points = ? WHERE user_id = ?"""
    cursor.execute(query, [points, user_id])
    con.commit()
    con.close()


    
    

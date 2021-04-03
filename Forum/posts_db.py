import sqlite3 as sl
from datetime import datetime

#Gets posts from the database
def get_posts(forum_name):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT * FROM POSTS WHERE forum_name = ?"""
    cursor.execute(query, [forum_name])
    result = cursor.fetchall()
    con.close()
    return result

#retrieves comments from the database
def get_comments(post_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT * FROM REPLIES WHERE post_id = ? AND reply_parent_id IS NULL"""
    cursor.execute(query, [post_id])
    result = cursor.fetchall()
    con.close()
    return result

#Retrieves the replies to a comment from the database
def get_replies(reply_parent_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT * FROM REPLIES WHERE reply_parent_id = ?"""
    cursor.execute(query,[reply_parent_id])
    result = cursor.fetchall()
    con.close()
    return result

#Adds a comment or a reply. If it's a comment reply_parent_id is Null
def add_comment_or_reply(content, user_id, post_id, reply_parent_id):
    created_at = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """INSERT INTO REPLIES (user_id, post_id, content, created_at, likes, reply_parent_id) VALUES(?,?,?,?,?,?) """
    cursor.execute(query, [user_id, post_id, content, created_at, 0, reply_parent_id])
    con.commit()
    con.close()

#Adds a like to the post and stores the fact a user likes the post
def add_like_post(user_id, post_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """INSERT INTO LIKES_POST(user_id,post_id) VALUES (?,?)"""
    cursor.execute(query, [user_id, post_id])
    con.commit()
    query = """ UPDATE POSTS SET likes = likes + 1 WHERE post_id = ?"""
    cursor.execute(query, [post_id])
    con.commit()
    con.close()

#Adds a like to the reply and stores the fact a user likes the reply
def add_like_reply(user_id, reply_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """INSERT INTO LIKES_REPLY(user_id, reply_id) VALUES (?,?)"""
    cursor.execute(query, [user_id, reply_id])
    con.commit()
    query = """UPDATE REPLIES SET likes = likes + 1 WHERE reply_id = ?"""
    cursor.execute(query, [reply_id])
    con.commit()
    con.close()

#Removes the appropriate like from the DB and deincrements the like value in posts
def remove_like_post(user_id, post_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM LIKES_POST WHERE user_id = ? AND post_id = ?"""
    cursor.execute(query, [user_id, post_id])
    con.commit()
    query = """UPDATE POSTS SET likes = likes - 1 WHERE post_id = ?"""
    cursor.execute(query, [post_id])
    con.commit()
    con.close()

#Removes the appropriate like from the DB and deincrements the like value in replies    
def remove_like_reply(user_id, reply_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM LIKES_REPLY WHERE user_id = ? AND reply_id = ?"""
    cursor.execute(query, [user_id, reply_id])
    con.commit()
    query = """UPDATE REPLIES SET likes = likes - 1 WHERE reply_id = ?"""
    cursor.execute(query, [reply_id])
    con.commit()
    con.close()

#Removes a comment from the database 
def remove_comment(reply_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """ DELETE FROM REPLIES WHERE reply_id = ?"""
    cursor.execute(query, [reply_id])
    con.commit()
    con.close()

#Removes any replies related to a comment
def remove_replies(reply_parent_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM REPLIES WHERE reply_parent_id = ?"""
    cursor.execute(query, [reply_parent_id])
    con.commit()
    con.close()

#Gets a users likes for a post
def get_user_likes_posts(user_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT post_id FROM LIKES_POST WHERE user_id = ?"""
    cursor.execute(query, [user_id])
    result = cursor.fetchall()
    con.close()
    return result

#Get all a posts likes
def get_post_likes(post_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """ SELECT post_id FROM LIKES_POST WHERE post_id = ?"""
    cursor.execute(query, [post_id])
    result = cursor.fetchall()
    con.close()
    return result

#gets the id's of comments the user liked
def get_user_likes_comments(user_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT reply_id FROM LIKES_REPLY WHERE user_id = ?"""
    cursor.execute(query, [user_id])
    result = cursor.fetchall()
    con.close()
    return result

#gets all the likes of a reply
def get_reply_likes(reply_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT reply_id FROM LIKES_REPLY WHERE reply_id = ?"""
    cursor.execute(query, [reply_id])
    result = cursor.fetchall()
    con.close()
    return result

#Adds a post to the database
def add_post(user_id,forum_name, title, content):
    created_at = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """INSERT INTO POSTS(user_id, forum_name, title, content, created_at, likes) VALUES (?,?,?,?,?,?)"""
    cursor.execute(query, [user_id, forum_name, title, content, created_at, 0])
    con.commit()
    con.close()

#Removes a post from the database    
def remove_post(post_id):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM REPLIES WHERE post_id = ?"""
    cursor.execute(query, [post_id])
    con.commit()
    query = """DELETE FROM POSTS WHERE post_id = ?"""
    cursor.execute(query, [post_id])
    con.commit()
    con.close()

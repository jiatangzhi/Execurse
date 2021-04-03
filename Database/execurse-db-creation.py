import sqlite3 as sl

con = sl.connect('Execurse.db')

with con:
        con.execute("""
            CREATE TABLE USER (
                user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                academic INTEGER,
                current_points INTEGER
            );
        """)
        con.execute("""
            CREATE TABLE POSTS (
                post_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                forum_name TEXT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                likes INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES USER(user_id),
                FOREIGN KEY(forum_name) REFERENCES FORUMS(forum_name)
            );
        """)
        con.execute("""
            CREATE TABLE LIKES_POST(
                user_id INTEGER,
                post_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES USER(user_id),
                FOREIGN KEY(post_id) REFERENCES POSTS(post_id)
            );
        """)
        con.execute("""
             CREATE TABLE FORUMS (
                forum_name TEXT NOT NULL PRIMARY KEY
             );
        """)
        con.execute("""
            CREATE TABLE FOLLOWING (
                forum_name TEXT,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES USER(user_id),
                FOREIGN KEY(forum_name) REFERENCES FORUMS(forum_name)
            );
        """)
        con.execute("""
            CREATE TABLE REPLIES(
                reply_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                post_id INTEGER,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                likes INTEGER NOT NULL,
                reply_parent_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES USER(user_id),
                FOREIGN KEY(post_id) REFERENCES POSTS(post_id)
            );
        """)
        con.execute("""
            CREATE TABLE LIKES_REPLY(
                user_id INTEGER,
                reply_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES USER(user_id),
                FOREIGN KEY(reply_id) REFERENCES REPLIES(reply_id)
            );
        """)
        con.execute("""
            CREATE TABLE SUPPORT_EMAILS(
                email_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                support_email TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES USER(user_id)
            );
        """)

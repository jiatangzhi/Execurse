#from Question import Question
import random
import sqlite3 as sl
import datetime

question_prompts = [["What color are Apples?","(a) Red/Green","(b) Purple","(c) Orange","(d) rainbow","a"],
    ["What color are Bananas?", "(a) Orange","(b) Purple","(c) Yellow","(d) rainbow","c"],
    ["What color are Strawberries?","(a) Red/Green","(b) Purple","(c) Orange","(d) Red","d"],
    ["What Shape is the Earth?","(a) Square","(b) Circle","(c) Orange","(d) Round","d"],
    ["What is the name of the 8th planet from the sun?","(a) neptune","(b) saturn","(c) pluto","(d) uranus","a"],
    ["When I get multiplied by any number,the sum of the figures in the product is always me.What am I?","(a) 9","(b) 8","(c) 2","(d) 4","a"],
    ["What ten letter word starts with gas?","(a) Retirement","(b) Automobile","(c) Aberration","(d) Television","b"],
    ["Marvin was 13 years old in 1870 and 8 years old in 1875. How is it possible?","(a) The dates are in AC","(b) 1875 was a leap year","(c) 1870 began on the vernal equinox","(d) The dates are in BC","d"],
    ["What flies when it's born, lies when it's alive, and runs when it's dead","(a) A grain of sand","(b) An eaglet","(c) A snowflake","(d) A fruit fly","c"],
    ["I start with M, and end with X, and have a never ending amount of letters. What am I?","(a) Mix","(b) Mailbox","(c) Multiplex","(d) Matrix","b"],
    ["Rebecca weighs 98 pounds plus half her own weight. How much does she weigh?","(a) 128","(b) 196","(c) 192","(d) 184","b"],
    ["In Roman Numerals, how many hours in a day?","(a) XXVI","(b) XXIV","(c) XXIL","(d) XIXV","b"],
    ["What comes once in a minute, twice in a moment, but never in a thousand years?","(a) Thirty-one seconds","(b) 1/1000 of a decade","(c) One-tenth of a century","(d) The letter M","d"],
    ["What is 2+2?","(a) 1","(b) 2","(c) 3","(d) 4","d"],
    ["What is is the distance of the earth from the sun in (million kilometers)?","(a) 148.5","(b) 149.6","(c) 149.7","(d) 149.8","b"]]

def results_and_processing(list1,list2):
    '''
    5 points for every correct answer
    get all three correct and you get 30 points.
    this function takes in a two int strings and stores them
    '''
    score=0
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            score +=1
    if score == 3:
        score= score *10
    else:
        score= score *5
    
    return int(score)
    
def run_test(questions):
    score = 0
    for question in questions:
        answer = input(question.prompt)
        if answer == question.answer:
            score += 1
    print("You got "+ str(score) + "/"+str(len(questions))+"correct")

# GAMIFICATION FUNCTIONS
'''
They are called DAILY challenges for a reason
so first we make sure they get challenges on a daily or weekly basis
'''
#check if record exists in the table in question
#ususally if the record is not abvailable we can then create one
def check_username_already_used_in_table(table_name,user_name):
    '''

    :param table_name: name of target sql
    :param user_name: user_name in question
    :return:
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT user_name FROM """+table_name+""" WHERE user_name = ?"""
    cursor.execute(query, [user_name])
    result = cursor.fetchall()
    cursor.close()
    if len(result) == 0:
        return False
    else:
        return True

def date_verification_for_existing_challenger(table_name,user_name,timestep):
    '''
    the purpose of theis function is to check if the user has reached the required time for a new challenge or quiz
    :param user_name: unique identifier of the user in the database
    :param table_name: the name of the quiz or challenge table 
    :param timestep:  determines how often we want an event to occur e.g a daily timestep occours every day
    :return: first if else means true/false if a day has gone by
    :return: second if else means true/false if a week has gone by
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT date FROM """+table_name+""" WHERE user_name = ?"""
    cursor.execute(query, [user_name])
    result = cursor.fetchall()
    cursor.close()
    if len(result) != 0:
        datee =result[0][0]
        today = datetime.datetime.now().date()
        date_created = datetime.datetime.strptime(datee, "%Y-%m-%d").date()
        diff = (today -date_created).days
        if timestep == "daily":
            if diff >= 1:
                return True
            else:
                return False
        if timestep == "weekly":
            if diff >= 7:
                return True
            else:
                return False
    else:
        return True


def random_challenge_selector():
    '''
    :return:number of times challenges should be done
    '''
    numbers = []
    # make varying numbers of objectives
    #objectives = [["login","like_comments","reply_comment"],["add_post", "like_post", "add_comment"]]
    objectives = ["posts", "likes", "comments"]

    select = True
    while select:
        a = "0"
        b = str((random.randint(2, 4)))
        numbers.append(a + b)
        if len(numbers) == 3:
            select = False
    return numbers


# side function that allows us to increment text
def increment_text(text):
    if text != "Challenge Completed!":
        a= text[0]
        b= text[1]
        add = int(a) +1
        sum = str(add)+b
        if add >= int(b):
            return("Challenge Completed!")
        else:
            return(sum)
def daily_challenge_status_complete(user_name):
    '''

    :param user_name: this fuctiion takes just the user name to get his/her challenge category
    from that we are able to select key columns from the database and check if theyre "Completed"
    :return: True == Completed
    '''
    objectives = [["login","like_comments","reply_comments"],["add_posts", "like_posts", "add_comments"]]
    c_type=get_challenge_type(user_name)
    challenges= objectives[c_type]
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT """ + challenges[0] + """, """ + challenges[1] + """, """ + challenges[2] + """ 
        FROM DAILYCHALLENGES where user_name = ? """
    cursor.execute(query, [user_name])
    result = cursor.fetchall()
    list_to_check = list(result[0])
    con.close()
    sum = 0
    for i in range(len(list_to_check)):
        if list_to_check[i] == "Challenge Completed!":
            sum+=1
    if sum ==3:
        return True

def set_challenge_done(user_name):
    '''

    :param user_name: identifies specific row of the status column to mark if the user is done.
    :return: Nothing
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """UPDATE DAILYCHALLENGES SET status = (?) WHERE user_name = ?"""
    cursor.execute(query, ['true',user_name])
    con.commit()
    con.close()
    
def daily_challenge_status_check(user_name):
    '''

    :param user_name: identifies specific row of the status column to see if the user is done or not
    this function contributes to whether the user deserves a new challenge or not.
    :return: True means done False means the opposite
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT status FROM DAILYCHALLENGES where user_name = ? """
    cursor.execute(query, [user_name])
    result = cursor.fetchall()
    con.close()
    if result[0][0] == 'false':
        return False
    else:
        return True

#def get_users_challenge_type
def challenge_points_assignment_function(user_name,action):
    '''
    :param user_name: username identifies the rows
    :param action: identifies the column
    the key here is to extract the two digit sting from the database and increment the first number.
    indicating the user has made progress
    :return:
    '''
    objectives = [["login","like_comments","reply_comments"],["add_posts", "like_posts", "add_comments"]]
    c_type= get_challenge_type(user_name)
    challenges= objectives[c_type]
    for i in range(len(challenges)):
        if challenges[i] == action:
            con = sl.connect("Execurse.db")
            cursor = con.cursor()
            query = """SELECT """+challenges[i]+""" FROM DAILYCHALLENGES where user_name = ? """
            cursor.execute(query, [user_name])
            result = cursor.fetchall()
            con.commit()
            new_result= str(increment_text(result[0][0]))
            query = """UPDATE DAILYCHALLENGES SET ("""+challenges[i]+""") = (?) WHERE user_name = (?)"""
            cursor.execute(query,[new_result, user_name])
            con.commit()
            con.close()

def initiate_challenge_at_database(user_name):
    '''
    :param user_name: using the user_name, we create random daily challenges for the user
    :return: nothing , adds them To the DB
    '''
    today = str(datetime.datetime.now().date())
    objectives = [["login","like_comments","reply_comments"],["add_posts", "like_posts", "add_comments"]]
    challenge_type = random.randint(0, (len(objectives) - 1))
    numbers = random_challenge_selector()
    challenges= objectives[challenge_type]
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """INSERT INTO DAILYCHALLENGES (user_name, date, """+challenges[0]+""", """+challenges[1]+""",
    """+challenges[2]+""", challenge_type) VALUES (?,?,?,?,?,?)"""
    cursor.execute(query, [user_name, today, numbers[0], numbers[1], numbers[2], challenge_type])
    con.commit()
    cursor.close()

def get_challenge_type(user_name):
    '''

    :param user_name: using the username we can identify the specific coulumn in challenge_type.
    :return: int .this int is a number of the index of the list of challenges
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT challenge_type FROM DAILYCHALLENGES where user_name = ? """
    cursor.execute(query, [user_name])
    result = cursor.fetchall()
    con.close()
    return result[0][0]
def remove_old_challenge_record(user_name):
    '''

    :param user_name:
    :return: when a user is eligible for a new challenge, we remove the old one to make way for the new
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM DAILYCHALLENGES where user_name = ? """
    cursor.execute(query, [user_name])
    con.commit()
    con.close()
    
def create_daily_challenge(user_name):
    '''

    :param user_name: with only the username we can smartly apply some conditions to determine if
    he/she is eligible for new daily challenges
    :return:
    '''
    if check_username_already_used_in_table("DAILYCHALLENGES",user_name) == False:
        initiate_challenge_at_database(user_name)

    if check_username_already_used_in_table("DAILYCHALLENGES",user_name) == True:
        if date_verification_for_existing_challenger("DAILYCHALLENGES",user_name,"daily") == True:
            remove_old_challenge_record(user_name)
            initiate_challenge_at_database(user_name)

def get_daily_challenge_table(user_name):
    '''

    :param user_name: the user name gets c_type which helps us identify the challenge to display for the user
    :return:
    '''
    objectives = [["login","like_comments","reply_comments"],["add_posts", "like_posts", "add_comments"]]
    c_type= get_challenge_type(user_name)
    challenges= objectives[c_type]
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT """+challenges[0]+""", """+challenges[1]+""", """+challenges[2]+""" 
    FROM DAILYCHALLENGES where user_name = ? """
    cursor.execute(query, [user_name])
    result = cursor.fetchall()
    con.close()
    return list(result)

def quiz_status_verifier(user_name):
    '''
    just like with daily challenges, a status varifier helps us know if a user is ready for a new challenge
    :param user_name:
    :return:
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """SELECT status FROM DAILYQUIZ where user_name = ? """
    cursor.execute(query, [user_name])
    result = cursor.fetchall()
    con.close()
    if result[0][0] == 'false':
        return False
    else:
        return True

def the_quiz_has_been_taken(user_name):
    '''just like with daily challenges, this status varifier helps us know if a user is ready for a new QUIZ
    :param user_name:
    :return:
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """UPDATE DAILYQUIZ SET status = ? WHERE user_name = ?"""
    cursor.execute(query, ['true',user_name])
    con.commit()
    con.close()

def remove_old_challenge_record(user_name):
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM DAILYCHALLENGES WHERE user_name = ?"""
    cursor.execute(query, [user_name])
    con.commit()
    con.close()


def create_daily_quiz_instance(user_name):
    today = str(datetime.datetime.now().date())
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """INSERT INTO DAILYQUIZ (user_name, date) VALUES (?,?)"""
    cursor.execute(query, [user_name, today,])
    con.commit()
    cursor.close()


def update_quiz_instance(user_name):
    today = str(datetime.datetime.now().date())
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM DAILYQUIZ WHERE user_name = ?"""
    cursor.execute(query, [user_name])
    con.commit()
    query = """INSERT INTO DAILYQUIZ (user_name, date) VALUES (?,?)"""
    cursor.execute(query, [user_name, today])
    con.commit()
    cursor.close()


def points_adding_function_user_id(table_name,user_id,points):
	'''
	this is a universal points adding function. meaning it works for all tables
	:param table_name: name of table we are updating
	:param user_id: uniqe identity of user
	:param points: points to add
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT points FROM """+table_name+""" WHERE user_id = ?"""
	cursor.execute(query, [user_id])
	result1 = cursor.fetchall()
	current_points= result1[0][0]
	updated_points= current_points+ points
	query = """UPDATE """+table_name+""" SET points = ? WHERE user_id = ?"""
	cursor.execute(query, [updated_points,user_id])
	con.commit()
	con.close()

def create_weekly_board_member(user_name):
    if check_username_already_used_in_table("WEEKLYBOARD",user_name) ==False:
        today = str(datetime.datetime.now().date())
        con = sl.connect("Execurse.db")
        cursor = con.cursor()
        query = """INSERT INTO WEEKLYBOARD (user_name, date) VALUES (?,?)"""
        cursor.execute(query, [user_name,today])
        con.commit()
        cursor.close()

def points_adding_function_user_name(table_name,user_name,points):
    '''
    this is a universal points adding function. meaning it works for all tables
    :param table_name: name of table we are updating
    :param user_name: uniqe identity of user
    :param points: points to add
    '''
    if table_name == "WEEKLYBOARD":
        if check_username_already_used_in_table("WEEKLYBOARD", user_name) == True:
            con = sl.connect("Execurse.db")
            cursor = con.cursor()
            query = """SELECT points FROM """ + table_name + """ WHERE user_name = ?"""
            cursor.execute(query, [user_name])
            result1 = cursor.fetchall()
            current_points = result1[0][0]
            updated_points = current_points + points
            query = """UPDATE """ + table_name + """ SET points = ? WHERE user_name = ?"""
            cursor.execute(query, [updated_points, user_name])
            con.commit()
            con.close()

            
    if table_name == "USER":
        con = sl.connect("Execurse.db")
        cursor = con.cursor()
        query = """SELECT current_points FROM """ + table_name + """ WHERE username = ?"""
        cursor.execute(query, [user_name])
        result1 = cursor.fetchall()
        current_points = result1[0][0]
        updated_points = current_points + points
        if type(current_points) == 'NoneType':
            updated_points = points
        query = """UPDATE """ + table_name + """ SET current_points = ? WHERE username = ?"""
        cursor.execute(query, [updated_points, user_name])
        con.commit()
        con.close()
    else:
        create_weekly_board_member(user_name)
        con = sl.connect("Execurse.db")
        cursor = con.cursor()
        query = """SELECT points FROM """ + table_name + """ WHERE user_name = ?"""
        cursor.execute(query, [user_name])
        result1 = cursor.fetchall()
        current_points = result1[0][0]
        updated_points = current_points + points
        print(current_points, "CURRENT")
        print(updated_points, "UPDATED!")
        query = """UPDATE """ + table_name + """ SET points = ? WHERE user_name = ?"""
        cursor.execute(query, [updated_points, user_name])
        con.commit()
        con.close()

#run_test(questions)
def get_user_score(table_name,user_name):

	'''Get the score of the user currently logged in from a specific table I.E weekly score, dailyquiz etc
	Arguments:
		user_name(int): the user_name of the user currently logged in
	Returns:
		result(int):
			points of the user
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = "SELECT points FROM """+table_name+""" WHERE user_name = ?"""
	cursor.execute(query, [user_name])
	result = cursor.fetchall()
	con.close()
	return result[0][0]

def get_scores_for_weekly_table():
	'''Gets the scores of each user in descending order so the highest scorer
	is returned first and also does not get records where the score is 0.
	Arguments:
		Nothing
	Returns:
		result(list of tuples): returns empty list if everyone has 0 points
			username(str): the username that will be displayed on the leaderboard
			current_points(int): the current score of the user
	'''
	con = sl.connect("Execurse.db")
	cursor = con.cursor()
	query = """SELECT date FROM WEEKLYBOARD WHERE points > 0 
	ORDER BY points DESC"""
	cursor.execute(query)
	result = cursor.fetchall()
	con.close()
	return result

def table_reset_function():
    '''
    here we identify the oldest record in the WEEKLY DB to see if its seven days old or more
    if it is. we will reset the entire table to grade the new comming week
    :return: NOthing
    '''
    result= get_scores_for_weekly_table()
    time_step = 0
    for i in range(len(result)):
        if len(result[i]) != 0:
            today = datetime.datetime.now().date()
            date_created = datetime.datetime.strptime(result[i][0], "%Y-%m-%d").date()
            diff = (today - date_created).days
            if diff > time_step:
                time_step = diff
                if time_step >= 7:
                    reset_weekly_table()
                    
def reset_weekly_table():
    '''
    here we identify the oldest record in the WEEKLY DB to see if its seven days old or more
    if it is. we will reset the entire table to grade the new comming week
    :return: NOthing
    '''
    con = sl.connect("Execurse.db")
    cursor = con.cursor()
    query = """DELETE FROM WEEKLYBOARD """
    cursor.execute(query)
    con.commit()
    con.close()



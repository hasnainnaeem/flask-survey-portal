DB_PATH = 'assets/survey_data.db'
REVIEWS_PATH = 'static/files/reviews.csv'
QUESTIONS_PATH = 'static/files/questions.csv'


USER_TABLE = 'users'
STMT_USER_TABLE = f'''CREATE TABLE IF NOT EXISTS {USER_TABLE}
                (netid int PRIMARY KEY, age int, internet_use int)'''


REVIEWS_TABLE = 'reviews'
STMT_REVIEWS_TABLE = f'''CREATE TABLE IF NOT EXISTS {REVIEWS_TABLE}
                    (id int PRIMARY KEY, statement text, type int)'''

STUDY_ONE_TABLE = 'study_one'
STMT_STUDY_ONE_TABLE = f'''CREATE TABLE IF NOT EXISTS {STUDY_ONE_TABLE}
                    (id int PRIMARY KEY, user_id int, review_id int, 
                                    question_id int, value int)'''


QUESTIONS_TABLE = 'questions'
STMT_QUESTIONS_TABLE = f'''CREATE TABLE IF NOT EXISTS {QUESTIONS_TABLE}
                    (id int PRIMARY KEY, statement text, type int, min text, max text)'''

STUDY_TWO_TABLE = 'study_two'
STMT_STUDY_TWO_TABLE = f'''CREATE TABLE IF NOT EXISTS {STUDY_TWO_TABLE}
                    (id int PRIMARY KEY, user_id int, question_id int, value int)'''

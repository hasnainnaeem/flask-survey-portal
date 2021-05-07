import db_config
import sqlite3

import pandas as pd

from logger import logger

class dbConnector():
    def __init__(self):
        self.db_path                = db_config.DB_PATH
        self.user_table             = db_config.USER_TABLE
        self.reviews_table          = db_config.REVIEWS_TABLE
        self.questions_table        = db_config.QUESTIONS_TABLE
        self.study_one_responses    = db_config.STUDY_ONE_TABLE
        self.study_two_responses    = db_config.STUDY_TWO_TABLE


    def build_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(db_config.STMT_USER_TABLE)
            c.execute(db_config.STMT_REVIEWS_TABLE)
            c.execute(db_config.STMT_STUDY_ONE_TABLE)
            c.execute(db_config.STMT_QUESTIONS_TABLE)
            c.execute(db_config.STMT_STUDY_TWO_TABLE)
            conn.commit()

            # load data from files into the database
            self.load_data(self.reviews_table, db_config.REVIEWS_PATH)
            self.load_data(self.questions_table, db_config.QUESTIONS_PATH)
    

    def load_data(self, table_name, file_path):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table_name}")
            
            results = c.fetchall()
            if len(results) > 0:
                print(f"Skipping insert in {table_name}...")
                return

            df = pd.read_csv(file_path)

            to_db = [tuple(x) for x in df.to_numpy()]

            c.executemany(f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join('?' for i in range(len(df.columns)))});", to_db)
            conn.commit()


    def add_user(self, netid, age, internet_use):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            try:
                c.execute(f"INSERT INTO users (netid, age, internet_use) VALUES ({netid}, {age}, {internet_use});")
                conn.commit()
            except Exception as e:
                logger.exception(e)
                return False

        return True
    
    def load_study1(self):
         with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table_name}")

    def get_questions(self, type):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            try:    
                questions = c.execute(f"SELECT * FROM questions WHERE type={type}")
            except Exception as e:
                print(e)
            
            question_rows = c.fetchall()
            return question_rows

    def get_reviews(self, type):
        review_codes = {"negative": 0, "positive": 1, "angry": 2, "anxious": 3}
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            try:    
                reviews = c.execute(f"SELECT * FROM reviews WHERE type={review_codes[type]}")
            except Exception as e:
                print(e)
            
            review_rows = c.fetchall()
            return review_rows

    def insert_study1(self, user_id, review_id, question_id, value):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            try:
                c.execute(f"INSERT INTO study_one (user_id, review_id, question_id, value) VALUES ({user_id}, {review_id}, {question_id}, {value});")
                conn.commit()
            except Exception as e:
                logger.exception(e)
                return False
        return True

    def insert_study2(self, user_id, question_id, value):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            try:
                c.execute(f"INSERT INTO study_two (user_id, question_id, value) VALUES ({user_id}, {question_id}, {value});")
                conn.commit()
            except Exception as e:
                logger.exception(e)
                return False
        return True
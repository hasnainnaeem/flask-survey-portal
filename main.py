import random

import dbConnector

from flask import Flask, render_template, flash, request, jsonify, redirect, session

from logger import logger

db = dbConnector.dbConnector()
db.build_tables()

app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SeCrEt'

@app.route("/verify_user", methods=['POST'])
def verify():
    request_type = request.headers['Content-Type']
    logger.info(request_type)
    response = False
    
    if "application/x-www-form-urlencoded" in request_type:
        netid = request.form.get('netid')
        age = request.form.get('age')
        internet_use = request.form.get('internet_use')
        response = db.add_user(netid, age, internet_use)

    if not response:
        return render_template('userinfo.html', user_exists=response, form_submitted=True)
    else:
        next_page = request.args.get("selection")
        if next_page == "study1":
            session[str(netid)+"-"+"study1"] = True
            return redirect('study1?userid='+str(netid))
        elif next_page == "study2":
            session[str(netid)+"-"+"study2"] = True
            return redirect('study2?userid='+str(netid))
        else:
            return ";)"


@app.route("/submit_study1", methods=['POST'])
def submit_study1():
    request_type = request.headers['Content-Type']
    logger.info(request_type)
    response = False
    question_id_answer = {} # dictionary containing id:answer pairs
    qid_rid_dic = {} # dictionay containing qid:rid pais

    # process type 1 squestions
    for j in range(6):
        answer = request.form.get(str(j)+"-"+"radio")
        question_id = request.form.get(str(j)+"-"+"qid")
        qid_rid_dic[question_id] = request.form.get(str(j)+"-"+"rid")

        if answer:
            question_id_answer[question_id] = answer[-1]
        else: # this statement isn't supposed to be executed but just a precaution
            # in front-end, make sure user selects an option
            # if user hasn't selected any option and front-end validation isn't used
            # assume the answer as neutral
            question_id_answer[question_id] = 5    
    
    userid = request.args.get("userid")

    for question_id, answer in question_id_answer.items():
        print(str(question_id)+" status: ")
        print(db.insert_study1(userid, qid_rid_dic[question_id], question_id, answer))
    
    session.pop(str(userid+"-study1"), None)
    print("Session for "+str(userid)+"released.")
    return render_template("thankyou.html")


@app.route("/submit_study2", methods=['POST'])
def submit_study2():
    request_type = request.headers['Content-Type']
    logger.info(request_type)
    response = False
    question_id_answer = {} # dictionary containing id:answer pairs

    # process type 2 questions
    for j in range(10):
        answer = request.form.get(str(2)+"-"+str(j)+"-"+"radio")
        question_id = request.form.get(str(2)+"-"+str(j)+"-"+"id")

        if answer:
            question_id_answer[question_id] = answer[-1]
        else: # this statement isn't supposed to be executed but just a precaution
            # in front-end, make sure user selects an option
            # if user hasn't selected any option and front-end validation isn't used
            # assume the answer as neutral
            question_id_answer[question_id] = 5    
    # process type 1 squestions
    for j in range(8):
        answer = request.form.get(str(1)+"-"+str(j)+"-"+"radio")
        question_id = request.form.get(str(1)+"-"+str(j)+"-"+"id")

        if answer:
            question_id_answer[question_id] = answer[-1]
        else: # this statement isn't supposed to be executed but just a precaution
            # in front-end, make sure user selects an option
            # if user hasn't selected any option and front-end validation isn't used
            # assume the answer as neutral
            question_id_answer[question_id] = 5    
    
    userid = request.args.get("userid")

    for question_id, answer in question_id_answer.items():
        print(str(question_id)+" status: ")
        print(db.insert_study2(userid, question_id, answer))
    
    session.pop(str(userid+"-study2"), None)
    print("Session for "+str(userid)+"released.")
    return "Form submitted successfully. Thank you for your time :)"


@app.route("/study1", methods=['GET', 'POST'])
def study1():
    userid=request.args.get("userid");

    # make sure user did not change id in the url
    if str(userid)+"-study1" in session:
        # store the question 1 fields in list variables
        review_types = ["positive", "negative", "anxious", "angry"]
        positive_rows = db.get_reviews("positive")
        negative_rows = db.get_reviews("negative")
        anxious_rows = db.get_reviews("anxious")
        angry_rows = db.get_reviews("angry")

        # Check which review's turn it is to be displayed
        # Taking reminder by 3 (total number of reviews of certain type)
        # will yeild the index for review whose turn is now
        angry_review_count = session["angry_review"]
        anxious_review_count = session["anxious_review"]
        negative_review_count = session["negative_review"]

        print("I'm inside")
        print(angry_review_count)
        print(anxious_review_count)
        print(negative_review_count)

        # increment for next session
        session["angry_review"] += 1
        session["anxious_review"] += 1
        session["negative_review"] += 1


        # random number to shuffle positive reviews
        ran_num = random.randint(0,3)

        # put non-positive reviews in a list
        review_list = [
            positive_rows[(ran_num)%3],
            angry_rows[angry_review_count%3],  
            positive_rows[(ran_num+1)%3], 
            anxious_rows[anxious_review_count%3], 
            positive_rows[(ran_num+2)%3],
            negative_rows[negative_review_count%3]
        ]
        
        # reviews are ready, now fetch questions
        question_rows = db.get_questions(1)

        # we need 6 questions. So, creating list of 6 randomly chosen questions
        ran_num = random.randint(0,6)
        
        question_list = []
        for i in range(6):
            question_list.append(question_rows[(ran_num+i)%6])

        # Question & review lists are ready. Now let's send them to template
        return render_template("study1.html", 
            userid=userid,
            question_list=question_list,
            review_list=review_list
        )
    else:
        return "Wrong netid."

@app.route("/study2", methods=['GET', 'POST'])
def study2():
    userid=request.args.get("userid");

    if str(userid)+"-study2" in session:
        # store the question 1 fields in list variables
        type_1_question_rows = db.get_questions(1)
        type_1_ids = []
        type_1_statements = []
        type_1_min = []
        type_1_max = []
        
        for row in type_1_question_rows:
            type_1_ids.append(row[0])
            type_1_statements.append(row[1])
            type_1_min.append(row[3])
            type_1_max.append(row[4])

        # store the question 2 fields in list variables
        type_2_question_rows = db.get_questions(2)
        type_2_ids = []
        type_2_statements = []
        type_2_min = []
        type_2_max = []
        
        for row in type_2_question_rows:
            type_2_ids.append(row[0])
            type_2_statements.append(row[1])
            type_2_min.append(row[3])
            type_2_max.append(row[4])

        return render_template("study2.html", 
            userid=userid,
            type_1_question_no=len(type_1_question_rows),
            type_1_ids=type_1_ids,
            type_1_statements=type_1_statements,
            type_1_min=type_1_min,
            type_1_max=type_1_max,
            type_2_question_no=len(type_2_question_rows),
            type_2_ids=type_2_ids,
            type_2_statements=type_2_statements,
            type_2_min=type_2_min,
            type_2_max=type_2_max,
        )
    else:
        return "Wrong netid."
    
@app.route("/userinfo", methods=["GET", "POST"])
def user_info():
    return render_template('userinfo.html', form_submitted=False, next_page=request.args.get("selection"))


@app.route("/", methods=["GET", "POST"])
def index():

    # to make sure each review in these types is shown equally
    try:
        if session["negative_review"] is None:
            pass
    except KeyError:
        session["negative_review"] = 0 # index of first review
    try:
        if session["angry_review"] is None:
            pass
    except KeyError:
        session["angry_review"] = 1
    try: 
        if session["anxious_review"] is None:
            pass
    except:
        session["anxious_review"] = 2

    print("I'm outside")
    print(session["angry_review"] )
    print(session["anxious_review"])
    print(session["negative_review"])
    return render_template("studyselection.html")

if __name__ == "__main__":
    app.run(debug=True)

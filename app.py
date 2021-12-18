from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *


app = Flask(__name__)
app.config['SECRET_KEY'] = "Nicj"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


RESPONSES = []
satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])
questions = satisfaction_survey.questions


@app.route("/")
def get_home_page():

    return render_template("home_page.html", survey=satisfaction_survey, r=RESPONSES)

# Routes for the first question


@app.route("/questions/0")
def get_question0():
    return render_template("question0.html", question=questions[0])


@app.route("/answer", methods=["POST", "GET"])
def save_first_question():
    answer = request.form["answer"]
    RESPONSES.append(answer)

    return redirect("/question/1")

# Routes for the second question


@app.route("/questions/1")
def get_question1():
    return render_template("question1.html", question=questions[1])


@app.route("/question/1", methods=["POST", "GET"])
def save_second_question():
    answer = request.form["answer"]
    RESPONSES.append(answer)

    return redirect("/question/2")

# Routes for the third question


@app.route("/questions/2")
def get_question2():
    return render_template("question2.html", question=questions[2])


@app.route("/question/2", methods=["POST", "GET"])
def save_third_question():
    answer = request.form["answer"]
    RESPONSES.append(answer)

    return redirect("/question/3")


# Routes for the fourth question
@app.route("/questions/3")
def get_question3():
    return render_template("question3.html", question=questions[3])


@app.route("/question/3", methods=["POST", "GET"])
def save_fourth_question():
    answer = request.form["answer"]
    RESPONSES.append(answer)

    return redirect("/thank-you")


@app.route("/thank-you")
def get_thank_you_page():
    return render_template("thank_you.html")

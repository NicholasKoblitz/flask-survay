from flask import Flask, request, render_template, redirect, session
from flask.helpers import flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *


app = Flask(__name__)
app.config['SECRET_KEY'] = "Nick"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


RESPONSES = "Answers"

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

    session[RESPONSES] = []

    return render_template("home_page.html", survey=satisfaction_survey, r=RESPONSES)


@app.route("/questions/<int:id>")
def get_question(id):
    answers = session.get(RESPONSES)

    if id != len(answers):
        flash("Invalid question ID")
        return redirect(f"/questions/{len(answers)}")

    else:
        question = questions[id]
        return render_template("question.html", question=question)


@app.route("/answer", methods=["POST", "GET"])
def save_question():

    answer = request.form["answer"]
    answers = session[RESPONSES]
    answers.append(answer)
    session[RESPONSES] = answers

    if len(answers) == len(questions):
        return redirect("/thank-you")
    else:
        return redirect(f"/questions/{len(answers)}")


@app.route("/thank-you")
def get_thank_you_page():
    return render_template("thank_you.html")

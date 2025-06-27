from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from model import granite_generate_response
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# In-memory storage
chat_history = []
sentiments = []
concerns = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    response, sentiment, submitted = "", "", False

    if request.method == "POST":
        if "question" in request.form:
            question = request.form["question"]
            response = granite_generate_response(question)
            chat_history.append((question, response))

        elif "feedback" in request.form:
            feedback = request.form["feedback"]
            polarity = TextBlob(feedback).sentiment.polarity
            sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
            sentiments.append(sentiment)

        elif "concern" in request.form:
            concern = request.form["concern"]
            concerns.append(concern)
            submitted = True

    return render_template("chat.html", history=chat_history, sentiment=sentiments[-1:] if sentiments else None, concern_submitted=submitted)

@app.route("/dashboard")
def dashboard():
    pos = sentiments.count("Positive")
    neg = sentiments.count("Negative")
    neu = sentiments.count("Neutral")
    return render_template("dashboard.html", pos=pos, neg=neg, neu=neu, concerns=concerns)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin":
            session["user"] = "admin"
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
import os

from flask import Flask, session, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":

        #Check if all fields were filled in
        if not request.form.get("name"):
            return render_template("sorry.html", error="Username field not filled in")

        elif not request.form.get("password"):
            return render_template("sorry.html", error="Password field not filled in")

        elif not request.form.get("passwordConfirm"):
            return render_template("sorry.html", error="Password confirmation field not filled in")

        #Get all fields from the form
        name = request.form.get("name")
        password = request.form.get("password")
        passwordConfirm = request.form.get("passwordConfirm")

        #Check form for correctness
        if not password == passwordConfirm:
            return render_template("sorry.html", error="Passwords did not match")

        return render_template("sucess.html", name=name)
    else:
        return render_template("register.html")

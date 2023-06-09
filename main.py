from flask import Flask, render_template, session, request, redirect, url_for
from db import Database, User, File
from passlib.hash import bcrypt
from pathlib import Path
import os
import string
import random
import uuid

ROOT_PATH = Path(__file__).parent

UPLOAD_FOLDER = ROOT_PATH / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
DB = Database()
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SECRET_KEY"] = os.urandom(24)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/')
def index():
    if not session.get("login"):
        session.login = None
    return render_template("index.html")


@app.route('/login', methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    if DB.check_for_user(email=email):
        user = DB.session.query(User).filter_by(email=email).first()
        if bcrypt.verify(password, user.password):
            session["login"] = True
            session["username"] = user.username
            return redirect(url_for("index"))
        else:
            return "Incorrect password"
    else:
        return "User does not exist"


@app.route('/register', methods=["POST"])
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    if DB.check_for_user(email, username):
        return "User already exists"
    pass_hash = bcrypt.hash(password)
    DB.create_new_user(email, username, pass_hash)
    return "User created"


@app.route("/logout")
def logout():
    session["login"] = False
    return redirect(url_for("index"))


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = f"{uuid.uuid4()}.jpg"  # use UUID to generate a unique filename
    filepath = app.config['UPLOAD_FOLDER'].joinpath(filename)
    file.save(filepath)
    return '', 204  # empty response with status code 204 to indicate success


def gen_access_token():
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(12))


if __name__ == "__main__":
    if not (ROOT_PATH / "access_token.txt").exists():
        with open("access_token.txt", "w") as f:
            f.write(gen_access_token())
    
    app.run(debug=True)

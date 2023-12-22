import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Needed for CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    two_factor_token = db.Column(db.String(64), nullable=True)
    google_account = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'    

@app.route("/")
def index():
    return render_template("index.html", current_user=None)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    return render_template("login.html", login_form=login_form)

@app.route("/about")
def about():
    return render_template("about.html")

class CreateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), validators.EqualTo('password', message='Passwords must match.')])
    submit = SubmitField("Create")


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    create_account_form = CreateAccountForm()
    if request.method == "GET":
        return render_template(
            "create_account.html", create_account_form=create_account_form
        )
    elif request.method == "POST":
        if create_account_form.validate_on_submit():
            input_username = create_account_form.username.data
            input_password = create_account_form.password.data
            hashed_password = generate_password_hash(input_password)
            new_user = User(username=input_username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for("login"))

def initialize_database():
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    if not os.path.exists(db_path):
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        initialize_database()

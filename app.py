from flask import Flask, render_template, redirect, url_for

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Needed for CSRF protection

@app.route("/")
def index():
    return render_template('index.html', current_user=None)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template('login.html', login_form=login_form)

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Create')

@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    create_account_form = CreateAccountForm()
    return render_template('create_account.html', create_account_form=create_account_form)

if __name__ == '__main__':
    app.run(debug=True)
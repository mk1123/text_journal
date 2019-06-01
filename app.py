# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request, _app_ctx_stack, render_template, url_for, flash, redirect
from urllib.parse import urlparse, urljoin
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
from flask_heroku import Heroku
from flask_login import LoginManager, login_user, login_required, current_user
from twilio.twiml.messaging_response import MessagingResponse
import sys

from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.secret_key = os.urandom(16)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/journal_entries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import Entry, User
from tables import Entries
from form import LoginForm

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.filter_by(username=user_id).first()
    except:
        return None
    
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("in here 1")
        sys.stdout.flush()
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print("in here 2")
            sys.stdout.flush()
            return redirect(url_for('login'))
        print(login_user(user, remember=form.remember_me.data))
        sys.stdout.flush()
        next_page = request.args.get('next')    
        if not is_safe_url(next_page):
            return flask.abort(400)
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('display_journal')
        print("should redirect")
        sys.stdout.flush()
        db.session.commit()
        return redirect(next_page)
    else:
        print(form.errors)
        sys.stdout.flush()
    return render_template('login.html', title='Sign In', form=form)



@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response

    body = request.values.get('Body', None)
    phone_num = request.form['From']
    
    user = User.query.filter_by(phone_num=phone_num).first()
    
    if body[:10].lower() == "password: ":
        user.set_password(body[10:])
        db.session.commit()
        resp = MessagingResponse()
        resp.message("Thanks for changing your password! It's been updated in the database.")
        return str(resp)
    else:
        curr_date = datetime.now() - timedelta(hours=7)
        new_entry = Entry(user.name, curr_date, body)
        db.session.add(new_entry)
        db.session.commit()
        resp = MessagingResponse()

        # Add a message
        resp.message(
            "Thanks for your response! It's been saved in the database.")

        return str(resp)
    

@app.route("/")
@login_required
def display_journal():
    name = current_user.name
    entries = db.engine.execute("select * from entries where name='" + name + "'order by date desc").fetchall()
    table = Entries(entries)
    return render_template("entries.html", table=table, name=name)

if __name__ == "__main__":
    app.run(debug=True)

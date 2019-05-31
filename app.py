# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request, _app_ctx_stack, render_template, url_for
from urllib.parse import urlparse, urljoin
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
from flask_heroku import Heroku
from flask_login import LoginManager, login_user, login_required
from twilio.twiml.messaging_response import MessagingResponse

from datetime import datetime, timedelta
import os

login_manager = LoginManager()
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.secret_key = os.urandom(16)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/journal_entries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager.init_app(app)
heroku = Heroku(app)
db = SQLAlchemy(app)

from models import Entry, User
from tables import Entries

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.engine.execute("select * from users where username='" + user_id + "'").first()[0]
    except:
        return None
    
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response

    body = request.values.get('Body', None)
    phone_num = request.form['From']
    
    name = db.engine.execute("select name from users where phone_num='" + phone_num + "'").first()[0]
    curr_date = datetime.now() - timedelta(hours=7)
    new_entry = Entry(name, curr_date, body)
    db.session.add(new_entry)
    db.session.commit()
    resp = MessagingResponse()

    # Add a message
    resp.message(
        "Thanks for your response! It's been saved in the database.")

    return str(resp)


@app.route("/user_setup")
def user_setup():
    return db.session.query(User).all()
    

@app.route("/")
@login_required
def display_journal():
    qry = db.engine.execute("select * from users")
    users = qry.fetchall()
    return render_template('names.html', users=users)

@app.route("/user/<username>")
def show_user_profile(username):
    # show the user profile for that user
    name = db.engine.execute("select name from users where username='" + username + "'").first()[0]
    entries = db.engine.execute("select * from entries where name='" + name + "'order by date desc").fetchall()
    table = Entries(entries)
    return render_template("entries.html", table=table, name=name)

    


if __name__ == "__main__":
    app.run(debug=True)

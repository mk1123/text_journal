# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request, _app_ctx_stack, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col
from flask_heroku import Heroku
from twilio.twiml.messaging_response import MessagingResponse

from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/journal_entries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

from models import Entry, User
from tables import Entries


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

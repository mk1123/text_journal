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

from models import Entry
from tables import Entries


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response

    body = request.values.get('Body', None)
    phone_num = request.form['From']
    curr_date = datetime.now() - timedelta(hours=7)
    new_entry = Entry(phone_num, curr_date, body)
    db.session.add(new_entry)
    db.session.commit()
    resp = MessagingResponse()

    # Add a message
    resp.message(
        "Thanks for your response! It's been saved in the database.")

    return str(resp)

@app.route("/")
def display_journal():
    qry = db.session.query(Entry).order_by(Entry.date.desc())
    entries = qry.all()
    table = Entries(entries)
    return render_template('entries.html', table=table)
    


if __name__ == "__main__":
    app.run(debug=True)

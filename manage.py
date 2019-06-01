from flask_script import Manager
from twilio.rest import Client
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
import argparse

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

from models import User

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

account_sid = 'AC92cbcdb460fcb1606c06fcf92e013436'
auth_token = '509f7fea616ef52459984f9bd6271bcc'
client = Client(account_sid, auth_token)
twilio_phone = '+14152377478'

@manager.command
def update():
    client_phones = db.session.query(User.phone_num).all()
    for client_string in client_phones:
        message = client.messages.create(body="Hey man. How's your day going?",
                                        from_=twilio_phone,
                                        to=client_string)
        
@manager.command
def user_setup(phone_num, name):
    new_user = User(phone_num, name)
    db.session.add(new_user)
    db.session.commit()
    first_paragraph = "Welcome to Manan's Journal! I'm Jiminy. I'll ask you how your day's going every day\
                                     at 9PM, and feel free to respond however you want. I'll store your response, \
                                     so you can keep track of all your thoughts!"
    second_paragraph = "To see all your previous entries, go to http://manansjournal.herokuapp.com."
    third_paragraph = "You'll have to log in! Your username is " + new_user.username + ", but you'll have to \
                                    set your password. To set your password, send me a message like this:\n \
                                    password: <password>\n \
                                    where <password> is your new password. Your password is SHA256 encrypted, so the only \
                                    person that can see it is you."

    client.messages.create(from_=twilio_phone, to=phone_num, body=first_paragraph)
    client.messages.create(from_=twilio_phone, to=phone_num, body=second_paragraph)
    client.messages.create(from_=twilio_phone, to=phone_num, body=third_paragraph)

@manager.command
def reset_properties():
    users = User.query.all()
    for user in users:
        user.is_authenticated = False
        user.is_active = True
        user.is_anonymous = False
    db.session.commit()


if __name__ == "__main__":
    manager.run()
    if len(sys.argv) == 4:
        user_setup(*sys.argv[2:])
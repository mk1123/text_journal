from flask_script import Manager
from twilio.rest import Client
from flask_migrate import Migrate, MigrateCommand
import os
import argparse
from random import randint

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

from models import User, Entry
from datetime import datetime, timedelta

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

account_sid = 'AC92cbcdb460fcb1606c06fcf92e013436'
auth_token = '509f7fea616ef52459984f9bd6271bcc'
client = Client(account_sid, auth_token)
twilio_phone = '+14152377478'
list_of_messages = ['Hey! How are you doing today?', 'Greetings! Do you have a moment to talk about your day?', 'Hi! Tell me a pertinent fact about your day!']


@manager.command
def update2():
    active_users = db.session.query(User).filter(User.is_deleted == False).all()
    print(active_users)
    for user in active_users:
        client_string = user.phone_num
        # print(client_string)
        # print(user.name)
        user_exists = db.engine.execute("select date from entries where name='" + user.name + "'order by date desc").first()
        if user_exists:
            latest_entry = user_exists.date
            # print(latest_entry)
            if datetime.now() - latest_entry > timedelta(days=3):
                message = client.messages.create(body="Hey, haven't seen you in a while! Feel free to just hit me up any time you want to say something noteworthy or just pertinent. Future you won't regret it!",
                                            from_=twilio_phone,
                                            to=client_string)
                message = client.messages.create(body="Of course, if you don't want to hear from me anymore, just type 'unsubscribe' and I'll deactivate your account.",from_=twilio_phone,to=client_string)
                return
        
        message = client.messages.create(body=list_of_messages[randint(0, 2)],from_=twilio_phone,to=client_string)
        
@manager.command
def update():
    active_users = db.session.query(User).filter(User.is_deleted == False).all()
    # print(active_users)
    for user in active_users:
        client_string = user.phone_num
        # print(client_string)
        # print(user.name)
        message = client.messages.create(body=list_of_messages[randint(0, 2)],from_=twilio_phone,to=client_string)
            
        
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
                                    set your password. To set your password, send me a message like this:"
    fourth_paragraph = "password: <password>"
    fifth_paragraph = "where <password> is your new password. Your password is SHA256 encrypted, so the only \
                                    person that can see it is you."

    client.messages.create(from_=twilio_phone, to=phone_num, body=first_paragraph)
    client.messages.create(from_=twilio_phone, to=phone_num, body=second_paragraph)
    client.messages.create(from_=twilio_phone, to=phone_num, body=third_paragraph)
    client.messages.create(from_=twilio_phone, to=phone_num, body=fourth_paragraph)
    client.messages.create(from_=twilio_phone, to=phone_num, body=fifth_paragraph)

@manager.command
def reset_properties():
    users = User.query.all()
    for user in users:
        user.is_deleted = False
    db.session.commit()


if __name__ == "__main__":
    manager.run()
    if len(sys.argv) == 4:
        user_setup(*sys.argv[2:])
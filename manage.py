from flask_script import Manager
from twilio.rest import Client
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

from models import User

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

account_sid = 'AC92cbcdb460fcb1606c06fcf92e013436'
auth_token = '509f7fea616ef52459984f9bd6271bcc'
client = Client(account_sid, auth_token)

client_phones = ['+19256678140', '+19253536746', '+19255575551', '+19253519739']

@manager.command
def update():
    for client_string in client_phones:
        message = client.messages.create(body="Hey man. How's your day going?",
                                        from_='+14152377478',
                                        to=client_string)
        
@manager.command
def user_setup():
    japjot_name = User('+19253519739', "Japjot Singh")
    db.session.add(japjot_name)
    db.session.commit()
    return db.session.query(User).all()


if __name__ == "__main__":
    manager.run()
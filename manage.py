from flask_script import Manager
from twilio.rest import Client

from app import app

manager = Manager(app)
account_sid = 'AC92cbcdb460fcb1606c06fcf92e013436'
auth_token = '509f7fea616ef52459984f9bd6271bcc'
client = Client(account_sid, auth_token)

@manager.command
def update():
    message = client.messages.create(body="Hey man. How's your day going?",
                                     from_='+14152377478',
                                     to='+19256678140')


if __name__ == "__main__":
    manager.run()
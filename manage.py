from flask_script import Manager
from twilio.twiml.messaging_response import MessagingResponse

from app import app

manager = Manager(app)


@manager.command
def update():
    resp = MessagingResponse()

    # Add a message
    resp.message(
        "Hey man, how's your day been?")

    return str(resp)


if __name__ == "__main__":
    manager.run()
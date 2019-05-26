# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACc0992be06a604bbe3dc68ab082d6a56e'
auth_token = '0a7daa627643029779afec308d8531d9'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                    body="I love you so much beeber <3",
                    from_='+16507708365',
                    to='+19253536746'
                )

print(message.sid)

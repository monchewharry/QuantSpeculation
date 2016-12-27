from twilio.rest import TwilioRestClient
# put your own credentials here
ACCOUNT_SID = '<>'
AUTH_TOKEN = '<>'

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
    to = '16086221650',
    from_ = '16085120288',
    body = 'hello'
    )
        

from twilio.rest import TwilioRestClient
accountSid = <your_account_sid>
authToken = <your_auth_token>
twilioClient = TwilioRestClient(accountSid, authToken)
myTwilioNumber = <twilio_sender_number>
destCellPhone = <verified_receiver_number>
myMessage = twilioClient.messages.create(body = "whatever", from_=myTwilioNumber, to=destCellPhone)
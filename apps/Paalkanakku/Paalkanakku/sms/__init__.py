"""from twilio.rest import Client

account_sid = 'ACcce422ec8e6bc2c82333d2c8d16f9755'
auth_token = '3e283b775d15061c60d6076ec09ce54b'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+18173808816',
  body='Hello Alex',
  to='+918778400615'
)

print(message.sid)"""

# import required module
import requests
import json

# mention url
url = "https://www.fast2sms.com/dev/bulk"

# create a dictionary
my_data = {
  # Your default Sender ID
  'sender_id': 'FSTSMS',

  # Put your message here!
  'message': 'Hello Nith! Trying SMS!',

  'language': 'english',
  'route': 'p',

  # You can send sms to multiple numbers
  # separated by comma.
  'numbers': '9790438917, 8778400615, 8870505207'
}

# create a dictionary
headers = {
  'authorization': 'KOB8qoURLtxd73eWpcEuSY6ryG51MbAimsPk2gDTHaQVICnwFXcyqtZkKmbwM4I9eSCjQxzUofRHlpT5',
  'Content-Type': "application/x-www-form-urlencoded",
  'Cache-Control': "no-cache"
}

# make a post request
response = requests.request("POST",
							url,
							data = my_data,
							headers = headers)

print (response)
#load json data from source
#returned_msg = json.loads(response.text)

# print the send message
#print(returned_msg['message'])

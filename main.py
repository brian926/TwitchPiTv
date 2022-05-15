import os
import requests
import yaml
import json
from streamlink import Streamlink

# Load API keys
config = yaml.safe_load(open("config.yml"))

URL = "https://id.twitch.tv/oauth2/token"
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
GRANT_TYPE = "client_credentials"

# Setup Streamlink
session = Streamlink()

# Set Params to get access token using Client secret
PARAMS = {
  "client_id": CLIENT_ID,
  "client_secret": CLIENT_SECRET,
  "grant_type": GRANT_TYPE
}


r1 = requests.post(url = URL, params = PARAMS)

token = r1.json()["access_token"]

# Set Header with Client ID and Access Token
headers = {
    'Client-ID': CLIENT_ID,
    'Authorization': 'Bearer ' + token
}

# Make GET request from Twitch
streamer_name = "iitztimmy"
stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)

user = requests.get('https://api.twitch.tv/helix/users?login=brian92617', headers=headers)
#print(user.text)

# Get channels being followed and output all current live channels
followed = requests.get('https://api.twitch.tv/helix/users/follows?from_id=206770467&first=100', headers=headers)
obj = json.loads(followed.text)

liveCheck = "https://api.twitch.tv/helix/streams?"

# Go through all followed channels
for user in obj['data']:
    if 'to_name' in user:
        liveCheck += "user_login=" + user['to_name'] + "&"

 # Check if followed channels are live
check = requests.get(liveCheck, headers=headers)
checkTest = json.loads(check.text)
for live in checkTest['data']:
    if live['type'] == "live":
        print(live['user_login'] + " is " + live['type'] + " with " + str(live['viewer_count']) + " viewers")
        

# Extract streams
streams = session.streams("https://twitch.tv/{}".format(streamer_name))

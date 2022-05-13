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

# Get channels being followed
followed = requests.get("https://api.twitch.tv/helix/streams/followed", headers=headers)
obj = json.loads(followed)

name = []
for user in obj['data']:
    if 'user_id' in user:
        name.append(user['user_id'])

print(' '.join(name))


# Extract streams
streams = session.streams("https://twitch.tv/{}".format(streamer_name))

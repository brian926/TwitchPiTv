import os
import requests
import yaml
from streamlink import Streamlink

config = yaml.safe_load(open("config.yml"))

URL = "https://id.twitch.tv/oauth2/token"
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
GRANT_TYPE = "client_credentials"

PARAMS = {
  "client_id": CLIENT_ID,
  "client_secret": CLIENT_SECRET,
  "grant_type": GRANT_TYPE
}

r1 = requests.post(url = URL, params = PARAMS)

token = r1.json()["access_token"]

headers = {
    'Client-ID': CLIENT_ID,
    'Authorization': 'Bearer ' + token
}

streamer_name = "iitztimmy"

stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)
print(stream)
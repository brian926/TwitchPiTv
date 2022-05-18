import os
import requests
import yaml
import json
import time
import keyboard
import subprocess
from streamlink import Streamlink

def get_api():
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

    return headers

# Used to get user's ID
# user = requests.get('https://api.twitch.tv/helix/users?login=YourUserName', headers=headers)
# print(user.text)

def get_live_channels(headers):
    print(f"Started to get Streams Execution in {time.perf_counter() - start} seconds")
    # Get channels being followed and output all current live channels in order by view count
    followed = requests.get('https://api.twitch.tv/helix/users/follows?from_id=206770467&first=100', headers=headers)
    obj = json.loads(followed.text)

    liveCheck = "https://api.twitch.tv/helix/streams?"

    # Go through all followed channels
    for user in obj['data']:
        if 'to_name' in user:
            liveCheck += "user_login=" + user['to_name'] + "&"

     # Check if followed channels are live
    name=[]
    check = requests.get(liveCheck, headers=headers)
    checkTest = json.loads(check.text)
    for live in checkTest['data']:
        if live['type'] == "live":
            # print(live['user_login'] + " is " + live['type'] + " with " + str(live['viewer_count']) + " viewers")
            name.append(live['user_login'])

    print(f"Returned Streams Execution in {time.perf_counter() - start} seconds")
    return name

def play_stream(streamer):
    stream_to_play = 'streamlink --player-args "--fullscreen --play-and-exit" https://twitch.tv/{} best'.format(streamer)
    return stream_to_play

def run_stream():
    # Set streamer to first streamer, start by playing the first stream
    headers = get_api()
    currentStreamer = 0
    name = get_live_channels(headers)
    process = subprocess.Popen('streamlink --player-args "--fullscreen --play-and-exit" https://twitch.tv/{} best'.format(name[currentStreamer]))

    while True:
        print(f"Completed Execution in {time.perf_counter() - start} seconds")
        # Wait for an event, if event was a key down and was N go to next streamer
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'n':
            # Refresh live channels
            name = get_live_channels(headers)
            if currentStreamer == (len(name) - 1):
                currentStreamer = 0
                process.terminate()
                process = subprocess.Popen(play_stream(name[currentStreamer]))
            else:
                currentStreamer += 1
                process.terminate()
                process = subprocess.Popen(play_stream(name[currentStreamer]))
        # if B was pressed, go to last streamer
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'b':
            # Refresh live channels
            name = get_live_channels(headers)
            if currentStreamer == 0:
                currentStreamer = (len(name) - 1)
                process.terminate()
                process = subprocess.Popen(play_stream(name[currentStreamer]))
            else:
                currentStreamer -= 1
                process.terminate()
                process = subprocess.Popen(play_stream(name[currentStreamer]))
        # Exit if C was pressed
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'c':
            process.terminate()
            break

if __name__=='__main__':
    start = time.perf_counter()
    run_stream()
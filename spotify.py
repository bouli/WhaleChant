import os
import base64
import json
import urllib

import requests
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_access_token():
    # TODO: use not expired access token
    access_token = False
    try:
        print("-- getting access token --") # TODO: add logging
        token_url = "https://accounts.spotify.com/api/token"
        auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes)
        token_data = {
            "grant_type": "client_credentials"
        }
        token_headers = {
            "Authorization": f"Basic {auth_base64.decode('utf-8')}"
        }
        access_token = requests.post(token_url, data=token_data, headers=token_headers).json()
        access_token = access_token["access_token"]
        print("-- access token OK --")  # TODO: add logging
    except Exception as e:
        print(e) # TODO: add logging

    return access_token


def get_auth_header():
    access_token = get_access_token()
    if  not access_token:
        print("-- access token failed --") # TODO: add logging
        exit()
    return {
        "Authorization": f"Bearer {access_token}"
    }


def validate_response(response):
    if "error" in response:
        print(response["error"]) # TODO: add logging
        exit()

    return response

def search_track(track_name):
    url = "https://api.spotify.com/v1/search"
    params = {
        "type": "track",
        "limit": 5,
        "q": track_name,
        }
    url += "?" + urllib.parse.urlencode(params)

    response = requests.get(url, headers=get_auth_header())
    response = validate_response(response).json()

    response = response["tracks"]["items"][0]
    print(json.dumps(response, indent=2) ) # TODO: add logging)
    return response

def get_playlist(playlist_id):
    playlist_id = playlist_id.split("/")[-1]
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    response = requests.get(url, headers=get_auth_header())
    response = validate_response(response).json()

    print(json.dumps(response, indent=2) ) # TODO: add logging
    return response

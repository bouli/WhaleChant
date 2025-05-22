import os
import json

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("GOOGLE_YOUTUBE_API_KEY")

def search_track(track_name):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    response = youtube.search().list(
        q=track_name,
        part="id,snippet",
        maxResults=10,
        type="video"
    ).execute()
    print(json.dumps(response["items"][0], indent=2)) # TODO: add logging response)

    is_video = False
    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            is_video = True
            break

    if is_video:
        is_video = response["items"][0]["id"]["kind"] == "youtube#video"
        response = youtube.videos().list(
            part="statistics",
            id=response["items"][0]["id"]["videoId"]
        ).execute()

        print(json.dumps(response, indent=2)) # TODO: add logging response)
    else:
        response = None
    return response

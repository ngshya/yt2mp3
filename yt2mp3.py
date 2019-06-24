import requests
import json
import pickle
import os  

with open('settings.json') as f:
    d = json.load(f)
    id_playlist = d["id_playlist"]
    api_key = d["api_key"]

r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=25&playlistId=" + id_playlist + "&key=" + api_key)
tmp = json.loads(r.text)
vlist = [x["contentDetails"]["videoId"] for x in tmp["items"]]
while "nextPageToken" in tmp.keys():
    token_next_page = tmp["nextPageToken"]
    r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?pageToken=" + token_next_page + "&part=snippet%2CcontentDetails&maxResults=25&playlistId=" + id_playlist + "&key=" + api_key)
    tmp = json.loads(r.text)
    vlist.extend([x["contentDetails"]["videoId"] for x in tmp["items"]])

if os.path.isfile('vlist.pickle'):
    oldlist = pickle.load(open("vlist.pickle", "rb"))
else:
    oldlist = []

difflist = list(set(vlist).difference(set(oldlist)))
vlist = list(set(vlist).union(set(oldlist)))

if len(difflist) > 0:
    for x in difflist:
        exec_string = 'cd mp3 && youtube-dl --ignore-errors --skip-unavailable-fragments --no-overwrites --max-filesize 1g --extract-audio --audio-format "mp3" https://www.youtube.com/watch?v=' + x
        # print(exec_string)
        os.system(exec_string)

pickle.dump(vlist, open("vlist.pickle", "wb"))
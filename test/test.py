import json
import requests

with open("songs.json", "r") as f:
    data = json.load(f)
    for song in data:
        r = requests.post('http://localhost:5000/songs/', json=song)

    f.close()

with open("songratings.json", "r") as f:
    data = json.load(f)
    for rating in data:
        r = requests.post('http://localhost:5000/songs/rating/', json=rating)

    f.close()
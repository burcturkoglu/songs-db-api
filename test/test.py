import json
import requests
from requests_toolbelt.multipart import encoder

with open("songs.json", "r") as f:
	data = json.load(f)
	data = json.dumps(data)
	
	headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
	url = 'http://localhost:5000/songs/'

	r = requests.post(url, data=data, headers=headers)
	f.close()

with open("songratings.json", "r") as f:
	data = json.load(f)
	data = json.dumps(data)
	
	headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
	url = 'http://localhost:5000/songs/rating/'

	r = requests.post(url, data=data, headers=headers)

	f.close()
	
	

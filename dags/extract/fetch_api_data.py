import requests
import json

def fetch_data():
    url = 'https://api.covidtracking.com/v1/us/daily.json'
    response = requests.get(url)
    data = response.json()

    with open('data/raw_data.json', 'w') as f:
        json.dump(data, f)

import requests

def mapper():
    data = requests.get("https://europe-west1-craigstanton2.cloudfunctions.net/traveller_map")
    return data.text
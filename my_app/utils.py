from urllib.parse import quote
from bs4 import BeautifulSoup
import json
import requests


import requests

LINGVANEX_API_KEY = 'a_nvXtZJjlt4KHJ0hIK9TqGOVvj1jO08n4VvN358zabMNEeAMZmrWNAx2EHdy9wtKgQ84bCdVTeId9AV9h'
URL = "https://api-b2b.backenster.com/b1/api/v3/translate"

PAYLOAD = {
    "platform": "api",
    "from": "en_GB",
    "to": "ga_IE",
    "data": None,
    "enableTransliteration": True
}
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": LINGVANEX_API_KEY
}


def fetch_translation(english_text):
    PAYLOAD['data'] = english_text
    response = requests.post(URL, json=PAYLOAD, headers=HEADERS)

    try:
        return json.loads(response.text)
    except:
        return None


# Test
# query_str = "England is stupid, and my dog jumped through my window."
# test_1 = fetch_translation(query_str)
# print(test_1)


def fetch_ipa(irish_text):
    output = {
        "input": irish_text,
        "output": None,
    }
    irish_text_encoded = quote(irish_text)
    url = f"https://gphemsley.org/linguistics/ga/ortho2ipa/?text={irish_text_encoded}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        output_tag = soup.find('p', {'class': 'output'})

        if output_tag:
            output['output'] = output_tag.text

    return output

# # Test
# print(fetch_ipa(test_1['result']))

# # Unit test
# test_1['pronunciation'] = fetch_ipa(test_1['result'])['output']
# print(test_1)
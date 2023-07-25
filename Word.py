import requests


class Word:
    def __init__(self, word: str):
        self.word = word

    def get_meanings(self):
        dict_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        req = requests.Session()
        response = req.get(dict_url + self.word)

        if response.ok:
            meanings = response.json()[0]["meanings"]
            return meanings
        else:
            return response.status_code

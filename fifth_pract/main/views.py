from django.shortcuts import render
import requests
import json
import random

def index(request):
    return render(request, "main/index.html")


def get_characters():
    url = "https://swapi.dev/api/people/"
    r = requests.get(url)
    if r.status_code != 200: raise KeyError("Не удалось достучаться до сервера")
    res = []
    information = json.loads(r.text)
    res.extend(list(information["results"]))

    characters = [res[0], res[2], res[4]]
    d = {
        "hero1": {},
        "hero2": {},
        "hero3": {}
    }

    for i in range(len(characters)):
        character = characters[i]
        index = ["hero1", "hero2", "hero3"]
        d[index[i]] = {
            "name": character["name"],
            "height": character["height"],
            "mass": character["mass"],
            "hair_color": character["hair_color"],
            "skin_color": character["skin_color"],
            "eye_color": character["eye_color"],
            "birth_date": character["birth_year"],
            "sex": character["gender"],
        }
    
    return d

def character_page(request):
    characters_information = get_characters()
    return render(request, "main/characters.html", characters_information)

import requests
import json
import random
from pprint import pprint


while True:
    url = "https://swapi.dev/api/people/"
    r = requests.get(url)
    if r.status_code != 200: raise KeyError("Не удалось достучаться до сервера")
    characters = []

    information = json.loads(r.text)
    while information["next"] != None:
        characters.extend(list(information["results"]))
        url = information["next"]
        r = requests.get(url)
        if r.status_code != 200: raise KeyError("Не удалось достучаться до сервера")
        information = json.loads(r.text)
    else:
        print(information)
        break

rand_borders = [0, len(characters)-1]

rand_choice = [random.randint(rand_borders[0], rand_borders[1]) for _ in range(3)]
while len(set(rand_choice)) != len(rand_choice) != 3: 
    rand_choice = [random.randint(rand_borders[0], rand_borders[1]) for _ in range(3)]

choosen_characters = [characters[rand_choice[0]], characters[rand_choice[1]], characters[rand_choice[2]]]

d = {
    0: {},
    1: {},
    2: {}
}

for i in range(len(choosen_characters)):
    character = choosen_characters[i]
    d[i] = {
        "name": character["name"],
        "height": character["height"],
        "mass": character["mass"],
        "hair_color": character["hair_color"],
        "skin_color": character["skin_color"],
        "eye_color": character["eye_color"],
        "birth_date": character["birth_year"],
        "sex": character["gender"],
    }

pprint(d)
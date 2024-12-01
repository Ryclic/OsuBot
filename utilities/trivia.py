import pickle
from ossapi import *
from utilities.secrets_storage import *
from random import randint

api = Ossapi(OSU_CLIENT_ID, OSU_CLIENT_SECRET)

# (Difficulty - 1) * 50 = maps down in search
def select_map(difficulty):
    random_index = randint(0, 49)
    if difficulty == 1:
        maps = api.search_beatmapsets(sort="plays_desc", category="any", mode=-1)
        return maps.beatmapsets[random_index]
    else:
        file = open("cursors.obj", "rb")
        cursors = pickle.load(file)
        maps = api.search_beatmapsets(sort="plays_desc", category="any", mode=-1, cursor=cursors[difficulty-2])
        return maps.beatmapsets[random_index]
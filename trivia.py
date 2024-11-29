from ossapi import *
from secrets_storage import *
from random import randint

api = Ossapi(OSU_CLIENT_ID, OSU_CLIENT_SECRET)

# (Difficulty - 1) * 50 = maps down in search
def select_map(difficulty):
    maps = api.search_beatmapsets(sort="plays_desc", category="any", mode=-1)
    random_index = randint(0, 49)
    if difficulty == 1:
        return maps.beatmapsets[random_index]
    else:
        for i in range(0, difficulty):
            maps = api.search_beatmapsets(sort="plays_desc", category="any", mode=-1, cursor=maps.cursor)
        return maps.beatmapsets[random_index]
    
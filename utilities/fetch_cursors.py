import pickle
from ossapi import *
from utilities.secrets_storage import *
from random import randint

api = Ossapi(OSU_CLIENT_ID, OSU_CLIENT_SECRET)

# This function is used to pre-fetch all the cursors 
# for the top played maps in descending order,
# used for for faster load times.
def fetch_cursors(pages):
    maps = api.search_beatmapsets(sort="plays_desc", category="any", mode=-1)
    cursors = []
    for i in range(0, pages):
        print(i)
        cursors.append(maps.cursor)
        maps = api.search_beatmapsets(sort="plays_desc", category="any", mode=-1, cursor=maps.cursor)
    file = open("cursors.obj", "wb")
    pickle.dump(cursors, file)
    file.close()
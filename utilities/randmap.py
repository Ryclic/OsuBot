from ossapi import *
from datetime import datetime, timezone
from random import randint
from utilities.secrets_storage import *

api = Ossapi(OSU_CLIENT_ID, OSU_CLIENT_SECRET)

# Use the latest submitted WIP map to determine the latest beatmapset ID
def find_recent_id():
    wip_maps = api.search_beatmapsets(mode=0, category="wip")
    wip_maps_dates = []
    for i in range(50):
        wip_maps_dates.append((wip_maps.beatmapsets[i].submitted_date, wip_maps.beatmapsets[i].id))
    now_time = datetime.now(timezone.utc)
    
    latest_id = min(wip_maps_dates, key=lambda x: abs(x[0] - now_time))[1]
    return latest_id

def find_random_map():
    MIN_ID = 1
    MAX_ID = find_recent_id()
    while True:
        random_id = randint(1, MAX_ID)
        try:
            result = api.beatmapset(beatmapset_id=random_id)
            # Find only osu! regular maps
            if str(result.beatmaps[-1].mode) == "GameMode.OSU":
                break
        except:
            print("Invalid Beatmap - likely deleted!")
    return result

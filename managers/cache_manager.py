import json

import config

# data containers
cached_stats_data = None
cached_moveset_data = None
cached_alt_name_data = None
cached_rarity_data = None
cached_nature_data = None
cached_type_data = None
cached_weakness_data = None
cached_duelish_data = None
pokemon = None

# caches the data
async def cache_data():
    global cached_stats_data, cached_moveset_data, cached_alt_name_data, cached_rarity_data, cached_nature_data, cached_weakness_data, cached_type_data, cached_duelish_data

    pokemon = get_pokemon_name()
    cached_stats_data = get_all_stats()
    cached_moveset_data = get_all_moveset()
    cached_alt_name_data = get_all_alt_names()
    cached_rarity_data = get_all_rarity_data()
    cached_nature_data = get_all_nature_data()
    cached_type_data = get_all_type_data()
    cached_weakness_data = get_all_weakness_data()
    cached_duelish_data = get_all_duelish_data()

    
def get_pokemon_name():
    with open('data/pokemon.json', 'r') as file:
        return json.loads(file)
    
# returns all the stats from stats file
def get_all_stats():
    stats_file = open(config.STATS_FILE_LOCATION, "r")
    stats_data_raw = stats_file.read()
    stats_data = json.loads(stats_data_raw)

    return stats_data

# return all the moveset from the moveset file
def get_all_moveset():
    ms_file = open(config.MOVESET_FILE_LOCATION, "r")
    ms_data_raw = ms_file.read()
    ms_data = json.loads(ms_data_raw)

    return ms_data

# returns all the alt names from the alt name file
def get_all_alt_names():
    alt_name_file = open(config.ALT_NAME_FILE_LOCATION, "r")
    alt_name_data = json.loads(alt_name_file.read())

    return alt_name_data

# returns all the rarity data from the rarity file
def get_all_rarity_data():
    rarity_file = open(config.RARITY_FILE_LOCATION, "r")
    rarity_data = json.loads(rarity_file.read())

    return rarity_data

def get_all_nature_data():
    nature_file = open(config.NATURE_FILE_LOCATION, "r")
    nature_data = json.loads(nature_file.read())

    return nature_data

def get_all_type_data():
    with open(config.TYPE_FILE_LOCATION, "r") as type_file:
        type_data = json.loads(type_file.read())
        
        return type_data

def get_all_weakness_data():
    with open(config.WEAKNESS_FILE_LOCATION, "r") as weakness_file:
        weakness_data = json.loads(weakness_file.read())
        
        return weakness_data

def get_all_duelish_data():
    with open(config.DUELISH_POKEMON_FILE_LOCATION, "r") as duelish_file:
        duelish_data = json.loads(duelish_file.read())

        return duelish_data

import discord
import requests
import json

from config import NORMAL_COLOR, ERROR_COLOR, NO_IMAGE
from managers import cache_manager
from cog_helpers import general_helper

"""data structure used to store pokemon data"""

class PokeData:

    p_id = 0
    p_name = ""
    p_types = ""
    p_region = ""
    p_abilities = ""
    p_weight = 0.0
    p_height = 0.0
    image_link = ""
    p_info = ""
    p_stats = {}
    p_total_stats = 0
    p_evolution_chain = ""
    p_rarity = ""

class AbilityData:

    a_name : str = ""
    a_desc_short : str = ""
    a_desc : str = ""
    a_gen : str = ""

"""returns the data of pokemon fetched from api"""

async def get_poke_by_id(poke_id):

    is_shiny = False

    if poke_id == "":
        return None
    else:
        if type(poke_id) is not int:
            poke_id = poke_id.lower()

            # check for shiny query
            if poke_id.endswith("-shiny"):
                is_shiny = True
                poke_id = poke_id.removesuffix("-shiny")

    try:
        poke_id = cache_manager.cached_alt_name_data[poke_id]
    except:
        poke_id = poke_id

    poke = PokeData()

    general_link = "https://pokeapi.co/api/v2/pokemon/{0}".format(poke_id)
    general_response = requests.get(general_link)
    general_data = json.loads(general_response.text)

    species_link = general_data["species"]["url"]
    species_response = requests.get(species_link)
    species_data = json.loads(species_response.text)

    generation_response = requests.get("https://pokeapi.co/api/v2/generation/{name}/".format(name=species_data["generation"]["name"]))
    generation_data = json.loads(generation_response.text)

    evolution_response = requests.get(species_data["evolution_chain"]["url"])
    evolution_data = json.loads(evolution_response.text)

    poke.p_id = general_data["id"]

    # get name
    poke.p_name = general_data["name"].capitalize()

    # get height and weight
    poke.p_height = float(general_data["height"]) / 10
    poke.p_weight = float(general_data["weight"]) / 10

    # get types
    types = general_data["types"]
    for i in range(0, len(types)):
        poke.p_types += types[i]["type"]["name"].capitalize()

        if i != len(types) - 1:
            poke.p_types += "\n"

    # get_region
    poke.p_region = generation_data["main_region"]["name"].capitalize()

    # get abilities
    abilities = general_data["abilities"]
    for i in range(0, len(abilities)):
        poke.p_abilities += abilities[i]["ability"]["name"].capitalize()

        if i != len(abilities) - 1:
            poke.p_abilities += "\n"

    # get info
    all_info = species_data["flavor_text_entries"]
    poke.p_info = "*NULL*"
    for i in all_info:
        if i["language"]["name"] == "en":
            poke.p_info = i["flavor_text"]
            break

    # get image_link
    if not is_shiny:
        poke.image_link = general_data["sprites"]["front_default"]
    else:
        poke.image_link = general_data["sprites"]["front_shiny"]

    # get stats
    stats = general_data["stats"]
    for i in range(0, len(stats)):
        stat_name = stats[i]["stat"]["name"]
        stat_value = stats[i]["base_stat"]
        poke.p_total_stats += stat_value
        poke.p_stats[stat_name] = stat_value

    # get evolution chain
    evolution_chain = []
    chain_data = evolution_data["chain"]
    while chain_data != "":
        evolution_chain.append(chain_data["species"]["name"])
        try:
            chain_data = chain_data["evolves_to"][0]
        except:
            break
    for i in range(0, len(evolution_chain)):
        poke.p_evolution_chain += evolution_chain[i].capitalize()

        if i > len(evolution_chain) - 2:
            break
        else:
            poke.p_evolution_chain += "\n"

    # get rarity
    try:
        rarity = cache_manager.cached_rarity_data[poke.p_name.lower()]
        if rarity == "mythical" or rarity == "legendary" or rarity == "ultra beast":
            poke.p_rarity = rarity.capitalize()
        else:
            poke.p_rarity = "Common"
    except:
        poke.p_rarity = None

    return poke

"""returns the dex embed from a pokemon's id or name"""

async def get_dex_entry_embed(poke_data):
    max_character_width = 40

    if poke_data is None:
        return general_helper.get_info_embd("Breh, Whats this?", "> Provide a pokemon name like ```-aa dex aron```", color=ERROR_COLOR)

    embd = discord.Embed(color=NORMAL_COLOR)
    embd.title = "**{0} : {1}**".format(poke_data.p_id, poke_data.p_name)

    description = general_helper.wrap_text(max_character_width, poke_data.p_info)
    description += "\n"

    embd.add_field(
        name="Height",
        value="{h} m".format(h=poke_data.p_height),
        inline=True
    )
    embd.add_field(
        name="Weight",
        value="{w} kg".format(w=poke_data.p_weight),
        inline=True
    )
    embd.add_field(
        name="Region",
        value="{r}".format(r=poke_data.p_region),
        inline=True
    )
    embd.add_field(
        name="Type(s)",
        value="{t}".format(t=poke_data.p_types),
        inline=True
    )
    embd.add_field(
        name="Ability(s)",
        value="{a}".format(a=poke_data.p_abilities),
        inline=True
    )
    embd.add_field(
        name="Evolution",
        value="{evolution_chain}".format(evolution_chain=poke_data.p_evolution_chain),
        inline=True
    )

    stats_string = "```"
    stats_string += "HP  : {hp}".format(hp=poke_data.p_stats["hp"]).ljust(11, " ") + "| " + "Sp.Atk : {spatk}".format(spatk=poke_data.p_stats["special-attack"]).ljust(13, " ")
    stats_string += "\n"
    stats_string += "Atk : {atk}".format(atk=poke_data.p_stats["attack"]).ljust(11, " ") + "| " + "Sp.Def : {spdef}".format(spdef=poke_data.p_stats["special-defense"]).ljust(13, " ")
    stats_string += "\n"
    stats_string += "Def : {df}".format(df=poke_data.p_stats["defense"]).ljust(11, " ") + "| " + "Speed  : {spd}".format(spd=poke_data.p_stats["speed"]).ljust(13, " ")
    stats_string += "```"

    embd.add_field(name="Stats (Total : {total_stats})".format(total_stats=poke_data.p_total_stats), value=stats_string, inline=False)

    embd.description = description

    image_link = (poke_data.image_link if poke_data.image_link is not None else NO_IMAGE)
    embd.set_image(url=image_link)

    if poke_data.p_rarity is not None:
        embd.set_footer(text=f"Rarity : {poke_data.p_rarity}")

    return embd

def get_ability_data(ability:str) -> AbilityData:

    data = AbilityData()

    ability_link = f"https://pokeapi.co/api/v2/ability/{ability}"
    ability_response = requests.get(url=ability_link)
    ability_data = json.loads(ability_response.text)

    data.a_name = ability_data["name"]
    data.a_gen = (ability_data["generation"]["url"]).replace("https://pokeapi.co/api/v2/generation/", "").replace("/", "")

    for entry in ability_data["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            data.a_desc_short = entry["flavor_text"]

    for entry in ability_data["effect_entries"]:
        if entry["language"]["name"] == "en":
            data.a_desc = entry["effect"]

    return data


async def get_ability_embed(ability:str) -> discord.Embed:

    ability_data = get_ability_data(ability)

    embd = discord.Embed(title=ability_data.a_name.capitalize(), color=NORMAL_COLOR)

    embd.description = "Ability Overview \n\n"

    embd.description += f"**Generation** : {ability_data.a_gen}"

    embd.add_field(
        name="Description : ",
        value=general_helper.wrap_text(100, ability_data.a_desc_short),
        inline=False
    )

    embd.add_field(
        name="Details : ",
        value=ability_data.a_desc[0: 500] + " ...",
        inline=False
    )

    return embd

import json
import json_to_property_converter
from  Character import Character

file_path = [
    "characters/ben_hargreeves.json",
    "characters/abed_nadir.json",
    "characters/alice_cullen.json",
    "characters/amy_santiago.json",
    "characters/barney_stinson.json",
    "characters/bart_simpson.json",
    "characters/bellatrix_lestrange.json",
    "characters/ben_chang.json",
    "characters/brienne_of_tarth.json",
    "characters/chidi_anagonye.json",
    "characters/walter_white.json"
]


def get_characters():
    characters = []
    for f in file_path:
        # get character properties
        character_name = json_to_property_converter.get_character_name(f)
        character_desc = json_to_property_converter.get_character_desc(f)
        character_aliases = json_to_property_converter.get_character_aliases(f)
        character_id = json_to_property_converter.get_character_id(f)
        c = Character(character_id,character_name, character_desc, character_aliases)
        characters.append(c)

        # build and print output string
        ''' output = "Name: "+character_name+"\nDescription: "+character_desc+"\nAliases: "
        if character_aliases != "N/A":
            for i in character_aliases:
                output += "\n - "+ i
        else: 
            output+=character_aliases
    
        print(output)'''
    return characters

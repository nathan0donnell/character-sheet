import json
import json_to_property_converter
# declare file path to json
file_path = "characters/ben_hargreeves.json"

# get character properties
character_name = json_to_property_converter.get_character_name(file_path)
character_desc = json_to_property_converter.get_character_desc(file_path)
character_aliases = json_to_property_converter.get_character_aliases(file_path)

# build and print output string
output = "Name: "+character_name+"\nDescription: "+character_desc+"\nAliases: "
if character_aliases != "Error Finding Aliases":
    for i in character_aliases:
      output += "\n - "+ i
else: 
    output+=character_aliases

print(output)

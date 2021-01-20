import json

# opens the JSON file in read mode and returns it as a list
def open_json(file_path):
    try:
      with open(file_path, 'r') as myfile:
          data = myfile.read()
      return json.loads(data)
    except IOError:
        print("IOError Occurred")

# the character id is found as it is needed for navigating th JSON file
def get_character_id(file_path):
    try:
        character = open_json(file_path)
        for i in character['entities']:
            character_id = i
        return character_id
    except:
        return "Error Finding ID"

# the character name, in english, is found in the file and is returned as a string
def get_character_name(file_path):
    try:
        character = open_json(file_path)
        character_id = get_character_id(file_path)
        character_name = character['entities'][character_id]['labels']['en']['value']
        return character_name
    except:
        return "Error Finding Name"

# the character description, in english, is found in the file and is returned as a string
def get_character_desc(file_path):
    try:
        character = open_json(file_path)
        character_id = get_character_id(file_path)
        character_desc = character['entities'][character_id]['descriptions']['en']['value']
        return character_desc
    except:
        return "Error Finding Description"

# a list of aliases the character has, in english, is found in the file and is returned as a list of strings
def get_character_aliases(file_path):
    try:
        character = open_json(file_path)
        character_id = get_character_id(file_path)
        character_aliases = ["none"]  # needed to define list variable
        # going through a list of aliases and adding each value to our list
        for i in range(len(character['entities'][character_id]['aliases']['en'])):
            if i == 0:
              character_aliases[0] = character['entities'][character_id]['aliases']['en'][i]['value']
            else:
               character_aliases.append(
               character['entities'][character_id]['aliases']['en'][i]['value'])
        return character_aliases
    except:
        return "Error Finding Aliases"

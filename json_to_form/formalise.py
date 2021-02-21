import json
from flask import request

# js = JSON file in dictionary format
# Every name/value pair is dictionary with another key called type
# Path is where you are currently at in the dictionary
# file_path is the path to the file which we write to


def json_to_elements(js, char_form, path, label):
    if isinstance(js, dict):
        return dict_to_element(js, char_form, path, label)
    elif isinstance(js, list):
        return list_to_element(js, char_form, path, label)
    elif isinstance(js, str):
        return str_to_element(js, char_form, path, label)
    elif isinstance(js, int):
        return int_to_element(js, char_form, path, label)
    else:
        return -1


'''
        elif isinstance(js, float):
                return float_to_element(js, file_path, path)
        elif isinstance(js, bool):
                return bool_to_element(js, file_path, path)
        '''

# continue on in same fashion as above int_to_form, string_to_form and implement them as suitable.

# path_to_id method escapes the path converting it to an appropriate element name
# By using paths like urls we should be able to take submitted form data and fully reconstruct the original json just from the form ids and the paths


def path_to_id(path):
    # special characters list
    special_characters = ['!', '"', '#', '$', '%', '&', '\'',
                          '(', ')', '*', '+', ',', '-', '.', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~']

    # converting special characters to unicode value
    for i in special_characters:
        path = path.replace(i, ("--"+str(ord(i))+"-"))

    # Converts _ to __
    path = path.replace('_', '__')

    # Converts / to _
    path = path.replace('/', '_')
    return path


def id_to_path(eID):
    # Converts _ to /
    eID = eID.replace('_', '/')

    # Converts // to /
    eID = eID.replace('/', '/')

    # converting unicode value to special characters
    while '--' in eID:
        index = eID.index("--")  # find the special character indicator
        number = ""
        index += 2  # skip to the number part
        while eID[index].isdigit():
            number += eID[index]  # finding the unicode value
            index += 1
        specialCh = "--"+number+"-"
        # replacing unicode value with character
        eID = eID.replace(specialCh, chr(int(number)))
        # have to account for replacing "_-"+number+"_" with one character, decrease index by appropriate amount
        index -= len(number)+2
    return eID


def dict_to_element(js, char_form, path, label):
    # need to open char_form or else it will not be defined
    char_form.write("\n<ul><li><div id='" +
                    path_to_id(path)+"'><h3>"+label+"</h3>")
    for key in js:
        json_to_elements(js[key], char_form, path+"/"+str(key), str(key))
    char_form.write("\n</div></li></ul>")


def list_to_element(js, char_form, path, label):
    # placeholder code
    char_form.write("\n<div id='"+path_to_id(path)+"'><h3>"+label+"</h3>")
    for key, val in enumerate(js):
        json_to_elements(val, char_form, path+"/"+str(key),
                         str(key))  # needs to be cast or wont work
    char_form.write("\n</div></li></ul>")


def str_to_element(js, char_form, path, label):
    elementId = path_to_id(path)

    # adding html code
    char_form.write("\n<div id='"+elementId+"'>")
    char_form.write('\n<br><label for="' + elementId +
                    '">' + label.capitalize() + ":</label>")
    if len(js) > 15:
        char_form.write('\n<textarea id="' + elementId +
                        '" name=' + elementId +
                        '" rows = "3" cols = "40">' + js + "</textarea><br>")
    else:
        char_form.write('\n<input type="text" id="' + elementId +
                        '" name=' + elementId +
                        '" value="' + js + '"/><br>')
    char_form.write("\n</div>")


def int_to_element(js, char_form, path, label):
    elementId = path_to_id(path)

    # adding html code
    char_form.write("\n<div id='"+elementId+"'>")
    char_form.write('\n<br><label for="' + elementId +
                    '" name=' + elementId +
                    '" >' + label.capitalize() +
                    ":</label>")
    if len(str(js)) > 15:
        char_form.write('\n<textarea id="' + elementId +
                        '" name=' + elementId +
                        '" rows = "3" cols = "40">' +
                        str(js) + "</textarea><br>")
    else:
        char_form.write('\n<input type="text" id="' +
                        elementId+'" value="' + str(js) + '"/><br>')
    char_form.write("\n</div>")

# create form method with the file path to the JSON file


def create_form(jpath):

    # loading the JSON
    with open(jpath, "r") as read_file:
        jfile = json.load(read_file)

    # writes a new file that can be written to
    char_form = open(
        "character_form.txt", "w", encoding="utf-8"
    )

    # beginning of HTML Code
    char_form.write(

        '<!DOCTYPE html>\n' +
        '<html lang="en">\n' +
        '<head>\n' +
        '  <title>JSON Editor</title>\n' +
        '  <meta charset="utf-8">\n' +
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n' +
        '  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n' +
        '  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n' +
        '  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>\n' +
        '</head>\n' +
        '<body>\n' +

        '<h2>Character Form</h2>\n<form action="" method="POST">'
    )
    # adding converted jfile to HTML code
    json_to_elements(jfile, char_form, "", "")

    # end HTML code
    char_form.write(
        '\n<input type="submit" value="Update Changes">\n</form>\n' +
        '</body>\n' +
        '</html>\n'

    )
    char_form.close()


# parse form method with the feedback
def parse_form(feedback):
    jsonDict = {}
    for key in feedback:
        value = feedback[key]

        # parse the key to work out the structure that made it
        # "/entities/Q65924637/type" = "date"
        # "/entities/Q65924637" = "25th November 1987"

        path = id_to_path(key)
        pathParts = path.split('/')
        parent = jsonDict
        for ind, val in enumerate(pathParts):
            if(ind == 0):
                continue
            elif(ind == (len(pathParts)-1)):
                parent[pathParts[ind]] = value
            elif(pathParts[ind] in parent):
                parent = parent[pathParts[ind]]
            else:
                parent[pathParts[ind]] = {}
                parent = parent[pathParts[ind]]
    # opening a new JSON file and writing the dictionary to it
    jfile = open('feedback.json', "w")
    json.dump(jsonDict, jfile)

import json

# js = JSON file in dictionary format
# Every name/value pair is dictionary with another key called type
# Path is where you are currently at in the dictionary
# file_path is the path to the file which we write to


def json_to_elements(js, html_form, path, label):
    if isinstance(js, dict):
        return dict_to_element(js, html_form, path, label)
    elif isinstance(js, list):
        return list_to_element(js, html_form, path, label)
    elif js is None:
        return none_to_element(js, html_form, path, label)
    elif js is True or js is False:
        return bool_to_element(js, html_form, path, label)
    elif isinstance(js, str):
        return str_to_element(js, html_form, path, label)
    elif isinstance(js, int) or isinstance(js, float) or isinstance(js, complex):
        return number_to_element(js, html_form, path, label)
    else:
        return -1


def type_to_elements(js, html_form, path, label):
    if isinstance(js, dict):
        if 'type' in js:
            if js['type'] == 'Text':
                str_to_element(js, html_form, path, label)
            elif js['type'] == 'Number':
                number_to_element(js, html_form, path, label)
            elif js['type'] == 'Boolean':
                bool_to_element(js, html_form, path, label)
            elif js['type'] == 'Date':
                date_to_element(js, html_form, path, label)
            elif js['type'] == 'Image':
                image_to_element(js, html_form, path, label)
            '''
            # table conversion not implemented
            elif js['type'] == 'Table':
                table_to_element(js, html_form, path, label)
            '''
            
        else:
            json_to_elements(js, html_form, path, label)


# path_to_id method escapes the path converting it to an appropriate element name
# By using paths like urls we should be able to take submitted form data and fully reconstruct the original json just from the form ids and the paths


def path_to_id(path):
    # special characters list
    special_characters = ['!', '"', '#', '$', '%', '&', '\'',
                          '(', ')', '*', '+', ',', '.', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~']
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

def dict_to_element(js, html_form, path, label):
    if label != "":
        if('type' in js and 'value' in js and (len(js) == 2 or len(js)==4)) :
            type_to_elements(js, html_form, path, label)
        else:
            html_form.write("<div style=\"border: 2px solid #ccc;margin:15px; padding-top: 0px; padding-left: 20px;padding-bottom:20px;\" id='"+path_to_id(path) +
                            "'>\n<h3>"+label+"</h3>\n<ul style=\"list-style: none\">\n")
            for key in js:
                if str(key) != 'type':
                    html_form.write("<li class = " +
                                    path_to_id(path) + ">")
                # if isinstance(js[key], dict):
                    # if 'type' in js[key]:
                    #     type_to_elements(js[key], html_form, path+"/"+str(key), str(key))
                #   else:
                    json_to_elements(js[key], html_form,
                                    path+"/"+str(key), str(key))
                    html_form.write("</li>\n")
            html_form.write("</ul>\n</div>\n")
    else:
        for key in js:
            json_to_elements(js[key], html_form, path+"/"+str(key), str(key))


def list_to_element(js, html_form, path, label):
    html_form.write("<div id='"+path_to_id(path) +
                    "'>\n<h3> "+label+"</h3>\n<ul style=\"list-style: none\">")
    for key, val in enumerate(js):
        html_form.write("<li class = "+path_to_id(path) + ">")
        json_to_elements(val, html_form, path+"/"+str(key),
                         str(key))
        html_form.write("</li>")
    html_form.write("</ul>\n</div>\n")


def bool_to_element(js, html_form, path, label):

    elementId = path_to_id(path)
    html_form.write("\n<div id='"+elementId+"_div'>")

    if isinstance(js, dict):
        html_form.write('\n<br><label for = "' + elementId + '_value"' +
                        '>' + label.capitalize() + ":</label>")
        if js['value'] is True:
            html_form.write('<select style=\"margin-left:15px;\" name="' + elementId + '_value" id="' + elementId + '_value">' +
                            '<option value="True" selected>True</option>' +
                            '<option value="False">False</option>' +
                            '</select>')
        elif js['value'] is False:
            html_form.write('<select style=\"margin-left:15px;\" name="' + elementId + '_value" id="' + elementId + '_value">' +
                            '<option value="True">True</option>' +
                            '<option value="False" selected>False</option>' +
                            '</select>')
        html_form.write('\n<input type="hidden" id="' + elementId +
                        '_type" name="' + elementId +
                        '_type" value="Boolean">')
    else:
        html_form.write('\n<br><label for = "' + elementId + '"' +
                        '>' + label.capitalize() + ":</label>")
        if js is True:
            html_form.write('<select style=\"margin-left:15px;\" name="' + elementId + '" id="' + elementId + '">' +
                            '<option value="True" selected>True</option>' +
                            '<option value="False">False</option>' +
                            '</select>')
        elif js is False:
            html_form.write('<select style=\"margin-left:15px;\" name="' + elementId + '" id="' + elementId + '">' +
                            '<option value="True">True</option>' +
                            '<option value="False" selected>False</option>' +
                            '</select>')
    html_form.write("\n</div>")


def none_to_element(js, html_form, path, label):
    elementId = path_to_id(path)
    html_form.write("\n<div id='"+elementId+"_div'>")
    html_form.write('\n<br><label for="' + elementId +
                    '_value">' + label.capitalize() + ":</label>")
    if isinstance(js, dict):
        html_form.write('\n<input style=\"margin-left:15px;\" type="text" id="' + elementId +
                        '_value" name="' + elementId +
                        '_value"><br>')
        html_form.write('\n<input type="hidden" id="' + elementId +
                        '_type" name="' + elementId +
                        '_type" value="Text">')
    else:
        html_form.write('\n<input style=\"margin-left:15px;\" type="text" id="' + elementId +
                        '" name="' + elementId +
                        '"><br>')
    html_form.write("\n</div>")


def image_to_element(js, html_form, path, label):
    elementId = path_to_id(path)
    html_form.write("\n<div id='"+elementId+"_div'>")

    html_form.write('\n<img style = "margin-left:15px;padding:10px; border: 1px solid  #ccc;" src="' +
                    js['value']['src']+'" alt="'+js['value']['alt']+'" width="200" height="200"> <br>')
    # add button which opens file prompt accepting imgs

    html_form.write('\n<input type="hidden" id="' + elementId +
                    '_value_alt" name="' + elementId +
                    '_value_alt" value="'+js['value']['alt']+'">')
    html_form.write('\n<input type="hidden" id="' + elementId +
                    '_value_src" name="' + elementId +
                    '_value_src" value="'+js['value']['src']+'">')
    html_form.write('\n<input type="hidden" id="' + elementId +
                    '_type" name="' + elementId +
                    '_type" value="Image">')
    html_form.write("\n</div>")

'''
# table conversion not implemented
def table_to_element(js, html_form, path, label):
    elementId = path_to_id(path)
    html_form.write("\n<div id='"+elementId+"_div'>")
    html_form.write('\n<br><label for="' + elementId +
                    '_value">' + label.capitalize() + ":</label>")

    html_form.write('\n<input style=\"margin-left:15px;\" type="text" id="' + elementId +
                    '_value" name="' + elementId +
                    '_value"><br>')
    html_form.write('\n<input type="hidden" id="' + elementId +
                    '_type" name="' + elementId +
                    '_type" value="Table">')
    html_form.write("\n</div>")
'''

def date_to_element(js, html_form, path, label):
    elementId = path_to_id(path)
    html_form.write("\n<div id='"+elementId+"_div'>")
    html_form.write('\n<br><label for="' + elementId +
                    '_value">' + label.capitalize() + ":</label>")

    html_form.write('\n<input style=\"margin-left:15px;\" type="date" id="' + elementId +
                    '_value" name="' + elementId +
                    '_value" value ="'+js['value']+'"> <br >')
    html_form.write('\n<input type="hidden" id="' + elementId +
                    '_type" name="' + elementId +
                    '_type" value="Date">')
    html_form.write("\n</div>")


def str_to_element(js, html_form, path, label):
    elementId = path_to_id(path)
    # adding html code
    html_form.write("\n<div id='"+elementId+"_div'>")
   
    if isinstance(js, dict):
        html_form.write('\n<br><label for="' + elementId +
                        '_value">' + label.capitalize() + ":</label>")
        if len(js['value']) > 15:
            html_form.write('\n<textarea style=\"margin-left:15px;\" id="' + elementId +
                            '_value" name="' + elementId +
                            '_value" rows = "3" cols = "40">' + js['value'] + "</textarea><br>")
        else:
            html_form.write('\n<input style=\"margin-left:15px;\" type="text" id="' + elementId +
                            '_value" name="' + elementId +
                            '_value" value="' + js['value'] + '"><br>')
        html_form.write('\n<input type="hidden" id="' + elementId +
                        '_type" name="' + elementId +
                        '_type" value="Text">')
    else:
        html_form.write('\n<br><label for="' + elementId +
                        '">' + label.capitalize() + ":</label>")
        if len(js) > 15:
            html_form.write('\n<textarea style=\"margin-left:15px;\" id="' + elementId +
                            '" name="' + elementId +
                            '" rows = "3" cols = "40">' + js + "</textarea><br>")
        else:
            html_form.write('\n<input style=\"margin-left:15px;\" type="text" id="' + elementId +
                            '" name="' + elementId +
                            '" value="' + js + '"><br>')
    html_form.write("\n</div>")


def number_to_element(js, html_form, path, label):
    elementId = path_to_id(path)
    # adding html code
    html_form.write("\n<div id='"+elementId+"_div'>")
    
    if isinstance(js, dict):
        html_form.write('\n<br><label for="' + elementId +
                        '_value" >' + label.capitalize() + ":</label>")
        if 'min' in js and 'max' in js:
            html_form.write('\n<input style=\"margin-left:15px;\" type="number" step="any" id="' + elementId +
                            '_value" name="' + elementId +
                            '_value" value="' + str(js['value']) + '" min="'+str(js['min'])+'" max="'+str(js['max'])+'"><br>')
        else:
            html_form.write('\n<input style=\"margin-left:15px;\" type="number" step="any" id="' + elementId +
                            '_value" name="' + elementId +
                            '_value" value="' + str(js['value']) + '""><br>')
        html_form.write('\n<input type="hidden" id="' + elementId +
                        '_type" name="' + elementId +
                        '_type" value="Number">')
    else:
        html_form.write('\n<br><label for="' + elementId +
                        '" >' + label.capitalize() + ":</label>")
        html_form.write('\n<input style=\"margin-left:15px;\" type="number" step="any" id="' + elementId +
                        '" name="' + elementId +
                        '" value="' + str(js) + '"><br>')
    html_form.write("\n</div>")


# create form method with the file path to the JSON file
def dict_to_sidebar(jdict, path, label):
    res = ""
    for key in jdict:
        if isinstance(jdict[key], dict):
            if not('type' in jdict[key] and 'value' in jdict[key] and len(jdict[key]) == 2):

                res += '<button class=\"tablinks\" onclick="openTab(event,\''+path_to_id(
                    path)+"_"+str(key)+'\')">' + str(key)+'</button>\n'
                res += dict_to_sidebar(jdict[key], path+"/"+str(key), str(key))
    return res


def create_form(jpath):
    # loading the JSON
    with open(jpath, "r") as read_file:
        jfile = json.load(read_file)

    # writes a new file that can be written to
    html_form = open(
        "Website/index.html", "w", encoding="utf-8"
    )

    sidebarStr = "<div id = \"sidebar-wrapper\" class=\"tab w3-sidebar w3-bar-block w3-light-grey w3-card\" style=\"width:180px; \">\n"
    sidebarStr += dict_to_sidebar(jfile, "", "")
    sidebarStr += "</div>\n"

    # beginning of HTML Code
    html_form.write(

        '<!DOCTYPE html>\n' +
        '<html lang="en">\n' +
        '<head>\n' +
        '<title>JSON Editor</title>\n' +
        '<meta charset="utf-8">\n' +
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n' +
        '<link rel="stylesheet" href="css/style.css">\n' +
        '<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n' +
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">\n' +
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">\n' +
        '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n' +
        '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>\n' +
        '<script src = "scripts/script.js"></script>\n' +
        '</head>\n' +
        '<body onLoad="tabLoad  ()">\n' +
        '<div id=\"wrapper\">\n' +
        sidebarStr +
        '<div class="w3-container" style="margin-left:180px; width:800px;" id="page-content-wrapper">\n' +
        '<form action="#" method="POST">\n'
    )
    # adding converted jfile to HTML code
    json_to_elements(jfile, html_form, "", "")

    # end HTML code
    html_form.write(
        '<input type="submit" style="margin-top:15px;margin-left: 20px;margin-bottom:15px;" value="Update Changes">\n</form>\n' +
        '</div>\n' +
        '</div>\n' +
        '</body>\n' +
        '</html>\n'

    )
    html_form.close()




# parsing form 
def convert_type(jsonDict):
    for key in jsonDict:
        if isinstance(jsonDict[key], dict):
            if 'type' in jsonDict[key]:
                if jsonDict[key]['type'] == 'Text':
                    jsonDict[key]['value'] = str(jsonDict[key]['value'])
                elif jsonDict[key]['type'] == 'Number':
                    jsonDict[key]['value'] = float(jsonDict[key]['value'])
                elif jsonDict[key]['type'] == 'Boolean':
                    jsonDict[key]['value'] = bool(jsonDict[key]['value'])
            jsonDict[key] = convert_type(jsonDict[key])
        elif isinstance(jsonDict[key], str):
            is_int=True
            is_float=True
            dotcount =0
            if jsonDict[key] == 'True':
                jsonDict[key] = True
            elif jsonDict[key] == 'False':
                jsonDict[key] = False
            else:
                if len(jsonDict[key])<1:
                    is_int=False
                    is_float=False
                for c in jsonDict[key]:
                    if not c.isdigit():
                        is_int=False
                    if c=='.':
                        dotcount=dotcount+1
                if dotcount>1:
                    is_float = False
                if is_int is False:
                    is_float = False
                if is_int is True:
                    jsonDict[key] = int(jsonDict[key])
                if is_float is True and is_int is False:
                    jsonDict[key] = float(jsonDict[key])
                if jsonDict[key]=='':
                    jsonDict[key]=None
    return jsonDict

# parse form method with the feedback
def parse_form(feedback):
    jsonDict = {}
    for key in feedback:
        value = feedback[key]
        path = id_to_path(key)
        pathParts = path.split('/')  # create path parts list

        parent = jsonDict
        for ind, val in enumerate(pathParts):  # iterate through path parts
            if(ind == 0):
                continue
            elif(ind == (len(pathParts)-1)):
                parent[pathParts[ind]] = value
            elif(pathParts[ind] in parent):
                parent = parent[pathParts[ind]]
            else:
                parent[pathParts[ind]] = {}
                parent = parent[pathParts[ind]]
    jsonDict = convert_type(jsonDict)

    # opening a new JSON file and writing the dictionary to it
    jfile = open('feedback.json', "w")
    json.dump(jsonDict, jfile)
    jfile.close()

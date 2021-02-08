import json

# converting dictionary to form method
def json_to_form(jtext, iprev):
    i = iprev  # keeping track of index
    text = ""
    newI = 0  # keeps track of index over recursive steps
    is_label = True

    # iterating through every character in jtext
    while i < len(jtext):
        # white space check
        if jtext[i] == " ":
            i += 1

        # Quotation marks check - using both " and ' - used for values
        elif jtext[i] == '"' or jtext[i] == "'":
            i += 1
            name = ""
            while jtext[i] != '"' and jtext[i] != "'":
                name += jtext[i]
                if i < len(jtext):
                    i += 1
                else:
                    break
            if is_label:  # if its on the left side of the : sign
                text += (
                    '\n<br><label for="'
                    + name
                    + '" style="margin-right:30px; text-align:right">'
                    + name.capitalize()
                    + ":</label>"
                )
            elif len(name) > 15:  # if its on the right side of the : sign
                text += (
                    '\n<textarea name="'
                    + name
                    + 'desc" rows = "3" cols = "40" name = "desc">'
                    + name
                    + "</textarea><br>"
                )
            else:
                text += (
                    '\n<input type="text" id="name" name="'
                    + name
                    + 'name" value="'
                    + name
                    + '"/><br>'
                )
            is_label = True
            i += 1

        # Digit check - used for values such as IDs
        elif jtext[i].isdigit():
            num = ""
            while jtext[i].isdigit():
                num += jtext[i]
                i += 1
            text += (
                '\n<input type="text" id="name" name="'
                + num
                + '" value="'
                + num
                + '"/>'
            )
            is_label = True

        # colon check - indicates equality
        elif jtext[i] == ":":
            is_label = False
            i += 1

        # open curly brackets check - indicates a new dictionary
        elif jtext[i] == "{":
            arr = json_to_form(jtext, i + 1)
            subsection_text = arr[0]
            i = arr[1]
            # subsection_text = subsection_text.replace("\n<br>", "\n<br>") #
            text+="<div style=\"padding: 20px;\">"
            text += subsection_text

        # close curly brackets check - indicates a dictionary closing
        elif jtext[i] == "}":
            i += 1
            newI = i
            text+="</div>"
            return [text, newI]

        # open hard brackets check - indicates a new array
        elif jtext[i] == "[":
            # text += "[\n<br>"
            i += 1
        # close hard brackets check - indicates an array closing
        elif jtext[i] == "]":
            # text += "]"
            i += 1

        # comma check - indcates an attributes ending
        elif jtext[i] == ",":
            text += "\n<br>"
            is_label = True
            i += 1

        # catching all other characters - error handling
        else:
            text += ""
            i += 1

    return [text, newI]


# create form method with the file path to the JSON file
def create_form(jpath):
    with open(jpath, "r") as read_file:
        jfile = json.load(read_file)  # loading the JSON
    char_form = open(
        "character_form.txt", "w", encoding="utf-8"
    )  # writes a new file that can be written to
    char_form.write(
        '<h2>Character Form</h2>\n<form action="submitted.php" method="post">'
    )  # beginning of HTML Code
    arr = json_to_form(str(jfile), 0)
    char_form.write(arr[0])  # adding converted jfile to HTML code
    char_form.write(
        '\n<input type="submit" value="Update Changes">\n</form>'
    )  # end HTML code
    char_form.close()
    return char_form


create_form("characters\\bart_simpson.json")
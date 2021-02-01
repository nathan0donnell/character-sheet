import json

def json_to_form(jtext, iprev):
    i = iprev
    text = ""
    newI = 0 # keeps track of index over recursive steps
    # iterating through every character in jtext
    while (i < len(jtext)):
        # white space check
        if jtext[i] == " ":
           # text += "\n"
            i += 1

        # Quotation marks check - using both " and ' - used for values
        elif jtext[i] == '"' or jtext[i] == '\'':
            i += 1
            while(jtext[i] != '"' and jtext[i] != '\''):
                text += jtext[i]

                if len(text) < len(jtext):
                    i += 1
                else:
                    break

            i += 1
            #text += "\n"

        # Digit check - used for values such as IDs
        elif jtext[i].isdigit():
            while jtext[i].isdigit():
                text += jtext[i]

                i += 1

        # colon check - indicates equality
        elif jtext[i] == ':':
            text += "="
            i += 1

        # open curly brackets check - indicates a new dictionary
        elif jtext[i] == '{':
            arr = json_to_form(jtext, i+1)
            subsection_text = arr[0]
            i = arr[1]
            subsection_text = subsection_text.replace("\n", "\n\t")
            text += subsection_text

        # close curly brackets check - indicates a dictionary closing
        elif jtext[i] == '}':
            i += 1
            newI = i
            return [text, newI]

        # open hard brackets check - indicates a new array
        elif jtext[i] == '[':
            text += "[\n"
            i += 1
        # close hard brackets check - indicates an array closing
        elif jtext[i] == ']':
            text += "]"
            i += 1

        # comma check - indcates an attributes ending
        elif jtext[i] == ',':
            text += "\n"
            i += 1

        # catching all other characters - error handling
        else:
            text += ""
            i += 1

    return [text, newI]


with open("characters/ben_hargreeves.json", "r") as read_file:
    ben = json.load(read_file)  # loading the json

# writes a new file that holds the output of method, encoding value is needed as default encoding causes error when writing
write_to = open("character_out.txt", "w", encoding="utf-8")
text = json_to_form(str(ben), 0)[0]
write_to.write(text)
write_to.close()

class Character:
    def __init__(self, name, desc, aliases):
        self.name = name
        self.desc = desc
        self.aliases = aliases
        # could add more properties later, these are just basics
    
    # method formalising character data
    def print_details(self):
        out = "Name: "+self.name +"\nDescription: "+self.desc + "\nAliases: "
        if self.aliases is list:
            for i in self.aliases:
                out += "\n - "+i
        elif self.aliases == "N/A":
            out+= "No Known Aliases"
        return out

    # method turning data into HTML form
    def htmlify_character(self):
        out="HTML code here" # add in HTML code translation - labels and textboxes for each property
        return out
class Character:
    def __init__(self, cid,name, desc, aliases):
        self.cid=cid
        self.name = name
        self.desc = desc
        self.aliases = aliases
      
        # could add more properties later, these are just basics

    # method formalising character data
    def print_details(self):
        out = "Name: "+self.name + "\nDescription: "+self.desc + "\nAliases: "
        if self.aliases is list:
            for i in self.aliases:
                out += "\n - "+i
        elif self.aliases == "N/A":
            out += "No Known Aliases"
        return out

    # method turning data into HTML form
    def htmlify_character(self):
        
        out = "<br /><label for=\""+self.cid+"name\" style=\"margin-right:30px; text-align:right\">Name:</label>\n<input type=\"text\" id=\"name\" name=\""+self.cid+"name\" value=\""
        out+=self.name
        out+="\"/><br />\n<label for=\""+self.cid+"desc\" style=\"display:inline-block;height:50px;margin-right:30px ;text-align:right\">Description:</label>\n<textarea name=\""+self.cid+"desc\" rows = \"3\" cols = \"40\" name = \"desc\">"
        out+=self.desc
        out+="</textarea><br>"
        
        return out

    # method turning data into PHP 
    def phpify_character(self):
        out="\nName: <?php echo $_POST[\""+self.cid+"name\"]; ?><br>\n"
        out+="Description: <?php echo $_POST[\""+self.cid+"desc\"]; ?><br>"
        return out
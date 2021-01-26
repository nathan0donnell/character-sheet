import Character
import json_testing

char_form = open("templates\character_form.html", "w")  # writes a new file that can be written to
char_form.write("<h2>Character Form</h2>\n<form action=\"submitted.php\" method=\"post\">")
characters=json_testing.get_characters()
for c in characters:
    char_form.write(c.htmlify_character())
char_form.write("\n<input type=\"submit\" value=\"Update Changes\">\n</form>")
char_form.close()


php_char = open("templates\\form_complete.php","w")
php_char.write("<html>\n<body>")
for c in characters:
    php_char.write(c.phpify_character())
php_char.write("\n</body>\n</html>")
php_char.close()
 
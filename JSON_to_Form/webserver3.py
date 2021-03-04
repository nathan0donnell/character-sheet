from flask import Flask,request
import formalise
import json
import mimetypes

mimetypes.types_map[".js"] = "application/javascript"

print(mimetypes.guess_type("style.js"))

app = Flask(__name__, static_url_path="", static_folder="httpdocs")

# @app.route("/<path:filename>")
# def access_file(filename):
# 	return send_from_directory("./httpdocs", filename)


@app.route("/", methods=['GET', 'POST'])
def start():
    formalise.create_form("characters/abed_nadir.json")
    char_form = open("character_form.txt", "r", encoding="utf-8")
    out = char_form.read()
    if request.method == 'POST':
        formalise.parse_form(request.form)
    return out


if __name__ == "__main__":
    app.run()

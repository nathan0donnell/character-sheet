from flask import Flask, request
import formalise
import json
import mimetypes

mimetypes.types_map[".js"] = "application/javascript"

print(mimetypes.guess_type("style.js"))

app = Flask(__name__, static_url_path="/", static_folder="./Website")
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# @app.route("/<path:filename>")
# def access_file(filename):
# 	return send_from_directory("./httpdocs", filename)


@app.route('/', methods=['GET', 'POST'])
def start():
    formalise.create_form("page-demo.json") # Parameter is the filepath to the JSON that will be displayed
    html_form = open("Website/index.html", "r", encoding="utf-8") # Getting the HTML file which was created by "formalise" method
    out = html_form.read()
    if request.method == 'POST':
        formalise.parse_form(request.form)
    return out


if __name__ == "__main__":
    app.run()

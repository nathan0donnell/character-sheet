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
    formalise.create_form("Formalisations/Person/Person.json")
    #formalise.create_form("page-demo.json")
    html_form = open("Website/index.html", "r", encoding="utf-8")
    out = html_form.read()
    if request.method == 'POST':
        f = open('rawdata.txt', "w")
        f.write(str(request.form))
        formalise.parse_form(request.form)
    return out


if __name__ == "__main__":
    app.run()

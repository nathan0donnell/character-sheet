from flask import Flask
import formalise
import mimetypes

mimetypes.types_map[".js"] = "application/javascript"

print(mimetypes.guess_type("style.js"))

app = Flask(__name__, static_url_path="", static_folder="httpdocs")

# @app.route("/<path:filename>")
# def access_file(filename):
# 	return send_from_directory("./httpdocs", filename)


@app.route("/hello")
def hello_world(name=None):
    return "Hello World!"


@app.route("/")
def start():
    formalise.create_form("characters\\bart_simpson.json")
    with open("character_form.txt", "r", encoding="utf-8") as f:
        out = f.read().replace("\n", " ")
    return out


if __name__ == "__main__":
    app.run()

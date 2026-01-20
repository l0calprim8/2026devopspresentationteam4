# Add to this file for the sample app lab
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session




sample = Flask(__name__)
sample.secret_key = "123"
sample.config["CLEARED_ON_START"] = False

@sample.before_request
def clear_once_per_start():
    if not sample.config["CLEARED_ON_START"]:
        session.clear()
        sample.config["CLEARED_ON_START"] = True
        
@sample.route("/")
def main():
    images = session.get("images", [])
    count = len(images)
    
    gallery = ""

    if images:
        if count % 2 == 0:
            gallery = '<div class="grid even">'
        else:
            gallery = '<div class="grid odd">'

        for img in images:
            gallery = gallery + (
                '<div class="card">'
                '<img src="/static/uploads/' + img + '">'
                '</div>'
            )

        gallery = gallery + '</div>'

    return render_template("index.html", gallery=gallery)

@sample.route("/add", methods=["GET"])
def add_page():
    return render_template("Add.html")


@sample.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("images")
    if not files:
        return redirect("/")

    images = session.get("images", [])

    for file in files:
        if not file or file.filename == "":
            continue
        filename = file.filename
        file.save("static/uploads/" + filename)
        images.append(filename)

    session["images"] = images
    return redirect("/")



if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080, threaded=True)

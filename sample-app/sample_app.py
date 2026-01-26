# Add to this file for the sample app lab
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import send_from_directory




sample = Flask(__name__)
sample.secret_key = "123"

UPLOAD_FOLDER = "uploads"

IMAGES_DB = "uploads/images.txt"

def load_images():
    try:
        with open(IMAGES_DB, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def save_images(images):
    with open(IMAGES_DB, "w") as f:
        for img in images:
            f.write(img + "\n")


@sample.route("/")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

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

    save_images(images)
    return redirect("/")



if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080, threaded=True)

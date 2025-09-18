from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/",methods=["GET"])
def index():
    result = ""
    image_url = ""

    return render_template ("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
 app.run (host="0.0.0.0", port=3000)
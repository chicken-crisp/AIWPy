from flask import Flask, request, render_template
import os
import uuid
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def ask_gemini(image_path):
    model = genai.GenerativeModel("gemini-2.0-flash")

    image = Image.open(image_path)

    prompt = "この料理1食分のカロリー、タンパク質、脂質を教えてください。料理名と数値と単位だけ簡潔に答えてください。"

    response = model.generate_content(
        [prompt, image],
        stream=False
    )
    return response.text

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    image_url = ""

    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = f"{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            result = ask_gemini(filepath)
            image_url = f"/static/uploads/{filename}"

    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

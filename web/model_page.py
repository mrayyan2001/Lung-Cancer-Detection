from tensorflow.keras.models import load_model
import cv2
from flask import Flask, render_template, request
import numpy as np
from PIL import Image

app = Flask(__name__)

model = load_model("./lung_cancer_model.h5")
cat = np.array(["Bengin cases", "Malignant cases", "Normal cases"])


def preprocessing(img):
    target_shape = (128, 128)
    img = cv2.resize(img, target_shape, interpolation=cv2.INTER_CUBIC)
    img = img.reshape(-1, *target_shape, 1)
    img = img / 255.0
    return img


def get_prediction(img):
    img = preprocessing(img)
    predict = model.predict(img)
    return f"{cat[predict.argmax()]}, {predict.max()*100:0.3f}%"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index", methods=["POST"])
def greet():
    if "file" not in request.files:
        return render_template("index.html")

    file = request.files["file"]
    if file.filename == "":
        return render_template("index.html")

    # open image using pillow library, then convert it to numpy array
    img = np.asarray(Image.open(file))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    prediction = get_prediction(img)
    return render_template("index.html", file=file, prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)

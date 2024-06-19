from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["UPLOAD_FOLDER"] = "web/static/uploads"

db = SQLAlchemy(app)


model = load_model("web\lung_cancer_final_model.h5")
cat = np.array(["Malignant cases", "Non-Malignant cases"])


def preprocessing(img):
    target_shape = (128, 128)
    img = cv2.resize(img, target_shape, interpolation=cv2.INTER_CUBIC)
    img = img.reshape(-1, *target_shape, 1)
    img = img / 255.0
    return img


def get_prediction(img):
    img = preprocessing(img)
    predict = model.predict(img)
    return f"{cat[np.round(predict).astype(int)][0]}, {(predict.max() if predict.max() > 0.5 else 1 - predict.max()) * 100:0.3f}%"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("signup"))

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists!", "danger")
            return redirect(url_for("signup"))

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists!", "danger")
            return redirect(url_for("signup"))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Congratulations, you are now a registered user!", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result2", methods=["GET", "POST"])
def result2():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "danger")
            return redirect(url_for("result2"))

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file", "danger")
            return redirect(url_for("result2"))

        try:

            if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                os.makedirs(app.config["UPLOAD_FOLDER"])

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            img = np.asarray(Image.open(file_path))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            prediction = get_prediction(img)

            return render_template(
                "result2.html", prediction=prediction, original_image=file.filename
            )
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for("result2"))

    return render_template("result2.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            return redirect(url_for("result2"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, request, jsonify
import flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, URLField, SelectField, DecimalField, BooleanField, FileField, EmailField
from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os
import datetime as dt


# key = os.urandom(26).hex()
# print(key)


app = Flask(__name__)
app.config["SECRET_KEY"] = "8b23dc14fc5e3e51e2a44d03daa7baacfded733e3a478e32f6af"
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)

API_KEY = "AIzaSyDZLgNIqOsSKk8k3rjcKylPpz4EvlOfLTI"
API_URL = "https://www.google.com/maps/embed/v1/MAP_MODE?key=AIzaSyDZLgNIqOsSKk8k3rjcKylPpz4EvlOfLTI"


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    map_url = db.Column(db.String)
    img_url = db.Column(db.String)
    location = db.Column(db.String)
    has_sockets = db.Column(db.Boolean, default=False, nullable=False)
    has_toilet = db.Column(db.Boolean, default=False, nullable=False)
    has_wifi = db.Column(db.Boolean, default=False, nullable=False)
    can_take_calls = db.Column(db.Boolean, default=False, nullable=False)
    coffee_price = db.Column(db.Float)
    seats = db.Column(db.String)


class AddCafe(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    map_url = URLField("Map", validators=[InputRequired()])
    img_url = URLField("Image", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    has_sockets = SelectField("Are there sockets?", choices=["yes", "no"], validators=[InputRequired()])
    has_toilet = SelectField("Is there a toilet?", choices=["yes", "no"], validators=[InputRequired()])
    has_wifi = SelectField("Does it have wifi?", choices=["yes", "no"], validators=[InputRequired()])
    can_take_calls = SelectField("Can you take calls?", choices=["yes", "no"], validators=[InputRequired()])
    coffee_price = DecimalField("Coffe Price", validators=[InputRequired()])
    seats = SelectField("How many seats are there?", choices=[("0-10"), ("10-20"), ("20-30"), ("30-40"), ("40-50"), ("50+")], validators=[InputRequired()])
    submit = SubmitField("Add Cafe")


class ReviewForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    message = TextAreaField("Your Review", validators=[InputRequired()])
    submit = SubmitField("Send")


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    cafe_id = db.Column(db.Integer)
    name = db.Column(db.String)
    message = db.Column(db.String)
    date = db.Column(db.String)


class RegisterForm(FlaskForm):
    name = StringField("Your Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    submit = SubmitField("Register now")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/all_cafes", methods=["GET", "POST"])
def get_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    list_cafe = []

    for cafe in all_cafes:
        cafe_dict = {
                "id": cafe.id,
                "name": cafe.name,
                "map_url": cafe.map_url,
                "img_url": cafe.img_url,
                "location": cafe.location,
                "seats": cafe.seats,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_wifi,
                "has_sockets": cafe.has_sockets,
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price,
        }
        list_cafe.append(cafe_dict)
    #print(list_cafe)
    return render_template("all_cafes.html", cafes=list_cafe)
# jsonify(cafes=list_cafe),


@app.route("/selected_cafe<int:cafe_id>", methods=["GET", "POST"])
def get_selected_cafe(cafe_id):
    selected_cafe = db.get_or_404(Cafe, cafe_id)
    # selected_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id))
    # selected_cafe = Cafe.id, cafe_id

    result_reviews = db.session.execute(db.select(Review).where(Review.cafe_id == cafe_id))
    selected_reviews = result_reviews.scalars().all()
    list_reviews = []
    for review in selected_reviews:
        review_dict = {
            "id": review.id,
            "name": review.name,
            "message": review.message,
            "cafe_id": review.cafe_id,
            "date": review.date
        }
        list_reviews.append(review_dict)
    #print(list_reviews)
    return render_template("cafe.html", cafe=selected_cafe, reviews=list_reviews, api_key=API_URL)


@app.route("/review<int:cafe_id>", methods=["GET", "POST"])
def write_review(cafe_id):
    #selected_place = db.get_or_404(Cafe, cafe_id)
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(
            name=request.form.get("name"),
            message=request.form.get("message"),
            cafe_id=cafe_id,
            date=dt.datetime.today().strftime('%B %d, %Y')
        )
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("get_cafes"))

    return render_template("review.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=request.form.get("password")
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
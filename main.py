from flask import Flask, render_template, redirect, url_for, request, jsonify
import flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, URLField, SelectField, DecimalField, BooleanField, FileField
from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os


# key = os.urandom(26).hex()
# print(key)


app = Flask(__name__)
app.config["SECRET_KEY"] = "8b23dc14fc5e3e51e2a44d03daa7baacfded733e3a478e32f6af"
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)


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

#
# with app.app_context():
#     db.create_all()


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


@app.route("/selected_cafe<int:cafe_id>", methods= ["GET", "POST"])
def get_selected_cafe(cafe_id):
    selected_cafe = db.get_or_404(Cafe, cafe_id)
    # selected_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id))
    # selected_cafe = Cafe.id, cafe_id

    return render_template("cafe.html", cafe=selected_cafe)


if __name__ == "__main__":
    app.run(debug=True)
import flask
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_bootstrap import Bootstrap5
# from flask_wtf import FlaskForm
# from sqlalchemy import ForeignKey
# from wtforms import StringField, TextAreaField, SubmitField, URLField, SelectField, DecimalField, BooleanField, EmailField
# from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os
import datetime as dt
from flask_gravatar import Gravatar
from forms import ReviewForm, LoginForm, RegisterForm, AddCafe


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


gravatar = Gravatar(app,
                    size=40,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    map_url = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    has_sockets = db.Column(db.Boolean, default=False, nullable=False)
    has_toilet = db.Column(db.Boolean, default=False, nullable=False)
    has_wifi = db.Column(db.Boolean, default=False, nullable=False)
    can_take_calls = db.Column(db.Boolean, default=False, nullable=False)
    coffee_price = db.Column(db.Float, nullable=False)
    seats = db.Column(db.String, nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    reviews = relationship("Review", back_populates="review_author")


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    cafe_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author_name = db.Column(db.String)
    review_author = relationship("User", back_populates="reviews")
    message = db.Column(db.Text)
    date = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_cafe", methods=["GET", "POST"])
@login_required
def add_cafe():
    form = AddCafe()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to add a café.")
            return redirect(url_for("login"))
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data,
            seats=form.seats.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("get_cafes"))
    return render_template("add_cafe.html", form=form)


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
    return render_template("all_cafes.html", cafes=list_cafe)


@app.route("/selected_cafe<int:cafe_id>", methods=["GET", "POST"])
def get_selected_cafe(cafe_id):
    selected_cafe = db.get_or_404(Cafe, cafe_id)

    result_reviews = db.session.execute(db.select(Review).where(Review.cafe_id == cafe_id))
    selected_reviews = result_reviews.scalars().all()
    list_reviews = []
    for review in selected_reviews:
        review_dict = {
            "id": review.id,
            "author_name": review.author_name,
            "message": review.message,
            "author_id": review.author_id,
            "cafe_id": review.cafe_id,
            "date": review.date
        }
        list_reviews.append(review_dict)
    return render_template("cafe.html", cafe=selected_cafe, reviews=list_reviews, current_user=current_user)


@app.route("/review<int:cafe_id>", methods=["GET", "POST"])
def write_review(cafe_id):
    form = ReviewForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to write a review.")
            return redirect(url_for("login"))

        new_review = Review(
            author_name=current_user.name,
            message=form.message.data,
            cafe_id=cafe_id,
            date=dt.datetime.today().strftime('%B %d, %Y')
        )
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("get_selected_cafe", cafe_id=cafe_id))

    return render_template("review.html", form=form, current_user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()

    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()

        if user:
            flash("You've already signed up with that email, log in instead.")
            return redirect(url_for("login"))

        hash_and_salted_pw = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=12
        )
        new_user = User(
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=hash_and_salted_pw,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()

        if not user:
            flash("This user does not exist. Please register.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=form, current_user=current_user)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("home"))
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

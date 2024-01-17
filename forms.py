from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import StringField, URLField, SubmitField, TextAreaField, EmailField
from wtforms.validators import InputRequired


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
    # name = StringField("Name", validators=[InputRequired()])
    message = TextAreaField("Your Review", validators=[InputRequired()])
    submit = SubmitField("Send")


class RegisterForm(FlaskForm):
    name = StringField("Your Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    submit = SubmitField("Register now")


class LoginForm(FlaskForm):
    email = EmailField("Your email", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    submit = SubmitField("Log in")


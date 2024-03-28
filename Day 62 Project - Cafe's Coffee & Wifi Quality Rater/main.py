from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = "Your secret key"
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = URLField("Cafe Location on Google Maps (URL)", validators=[DataRequired()])
    opening_time = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    closing_time = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating",
                                choices=["☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"],
                                validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating",
                                choices=["✘", "💪", "💪💪", "💪💪💪️", "💪💪💪💪", "💪💪💪💪💪"],
                                validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability",
                                choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                                validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_data = (f"\n{form.cafe.data}, {form.location_url.data}, {form.opening_time.data}, "
                     f"{form.closing_time.data}, {form.coffee_rating.data}, {form.wifi_rating.data}, "
                     f"{form.power_rating.data}")

        with open('cafe-data.csv', 'a', newline="", encoding="utf-8") as file:
            file.write(cafe_data)
            return redirect(url_for("cafes"), code=302)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding='utf-8') as csv_file:

        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run()

from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class AddSneakerForm(Form):
    sneaker_model_name = StringField('Sneaker Name', validators=[DataRequired()])
    sneaker_retail_price = IntegerField('Retail Price(JPY)', validators=[DataRequired()])
    sneaker_image = FileField('Sneaker Image', validators=[FileRequired()])


from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, validators, StringField, BooleanField, TextAreaField

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = IntegerField('Price', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    description = TextAreaField('Description', [validators.DataRequired()])
    colours = TextAreaField('Colours', [validators.DataRequired()])
    image_1 = FileField('Image_1', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg']), 'Product image'])
    image_2 = FileField('Image_2', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg']), 'Product image'])
    image_3 = FileField('Image_3', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg']), 'Product image'])

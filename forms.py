from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5


class AddNewCafe(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = URLField('Location URL', validators=[DataRequired()])
    image_url = URLField('Image Link', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = SelectField('Has Power Sockets?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    has_toilet = SelectField('Has Toilets?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    has_wifi = SelectField('Has Wifi?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    can_take_calls = SelectField('Can Take Calls?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    seats = StringField('Number of Seats', validators=[DataRequired()])
    coffee_price = StringField('Price of a Coffee', validators=[DataRequired()])
    submit = SubmitField('Add New Cafe')


class EditCafe(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = URLField('Location URL', validators=[DataRequired()])
    image_url = URLField('Image Link', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = SelectField('Has Power Sockets?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    has_toilet = SelectField('Has Toilets?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    has_wifi = SelectField('Has Wifi?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    can_take_calls = SelectField('Can Take Calls?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    seats = StringField('Number of Seats', validators=[DataRequired()])
    coffee_price = StringField('Price of a Coffee', validators=[DataRequired()])
    submit = SubmitField('Update Cafe')


class SearchCafeForm(FlaskForm):
    location = StringField('Location', render_kw={'style': 'width: 200px'}, validators=[DataRequired()])
    submit = SubmitField('Search')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Optional

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    place = StringField('Место', validators=[Optional()])
    image = FileField('Изображение', validators=[Optional()]) 
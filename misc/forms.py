from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError


class NewTaskForm(FlaskForm):
    label = StringField('Ajouter une tâche', validators=[DataRequired()])

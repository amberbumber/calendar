from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


#  форма переключения календаря
class CalendarForm(FlaskForm):
    pass


# форма для отправки жалоб/предложений
class HelpForm(FlaskForm):
    pass


# форма для создания события
class EventForm(FlaskForm):
    pass


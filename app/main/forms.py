from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField, StringField, TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired
from app.models import User
from datetime import date


#  форма переключения календаря
class CalendarForm(FlaskForm):
    month = SelectField('Месяц',
                        default=('', ''),
                        # default=date.today().month,
                        choices=[('', ''), (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'),
                                 (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'),
                                 (12, 'Декабрь')])
    year = SelectField('Год',
                       default='',
                       # default=date.today().year,
                       choices=['']+[year for year in range(1970, 2030)])
    submit = SubmitField('Показать')


# форма для отправки жалоб/предложений
class HelpForm(FlaskForm):
    pass


# форма для создания события
class EventForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()], format='%d.%m.%Y')
    summary = StringField('Название', validators=[DataRequired()])
    full_description = TextAreaField('Полное описание')
    submit = SubmitField('Сохранить')
    color = RadioField('Цвет',
                       choices=[('default', 'По умолчанию'), ('blue', 'Голубой'), ('green', 'Зеленый'),
                                ('yellow', 'Желтый'), ('orange', 'Оранжевый'), ('red', 'Красный'), ('pink', 'Розовый')],
                       validate_choice=False)

# пустая вспомогательная форма
class EmptyForm():
    submit = SubmitField('Submit')
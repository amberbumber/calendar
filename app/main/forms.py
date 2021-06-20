from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField, StringField, TextAreaField
from wtforms.validators import ValidationError, DataRequired
from app.models import User
from datetime import date


def month_name(id):
    months = {'1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май', '6': 'Июнь', '7': 'Июль',
              '8': 'Август', '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}
    return months[str(id)]


def month_id(month_name):
    months = {'Январь': '1', 'Февраль': '2', 'Март': '3', 'Апрель': '4', 'Май': '5', 'Июнь': '6', 'Июль': '7',
              'Август': '8', 'Сентябрь': '9', 'Октябрь': '10', 'Ноябрь': '11', 'Декабрь': '12'}
    return int(months[str(month_name)])


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

    # def validate_date(self):
    #     print(date.data)
    #     date.process_formdata(date.data)
    #     print(date.process_formdata(date.data))

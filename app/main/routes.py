from flask import current_app, render_template
from app.main import bp
from calendar import Calendar, month_name, LocaleTextCalendar
from datetime import date


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    c = LocaleTextCalendar(locale='ru')
    today_month_year = c.formatmonthname(date.today().year, date.today().month, width=0)
    week_days = [c.formatweekday(day, width=3) for day in range(0, 7)]
    return render_template('index.html', name='anna', c=c,
                           today_month_year=today_month_year, week_days=week_days)

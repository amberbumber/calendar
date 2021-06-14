from app.api import bp
from flask import jsonify, request, current_app
from calendar import LocaleTextCalendar
from datetime import date


@bp.route('/calendar', methods=['GET'])
def calendar():
    month = request.args.get('month', date.today().month)
    year = request.args.get('year', date.today().year)
    locale = request.args.get('locale', current_app.config['LANGUAGES'])
    c = LocaleTextCalendar(locale=locale)
    month_calendar = dict(
        year=year,
        month_number=month,
        month_name=c.formatmonthname(int(year), int(month), width=0).split()[0],
        week_days_name=[c.formatweekday(day, width=3).strip() for day in range(0, 7)],
        dates=[
            [dict(month=day.month, date=day.day) for day in week]
            for week in c.monthdatescalendar(int(year), int(month))
        ]
    )
    return jsonify(month_calendar)

from app.api import bp
from flask import jsonify, request, current_app, url_for
from calendar import LocaleTextCalendar, _nextmonth, _prevmonth
from datetime import date
from app.api.auth import token_auth


@bp.route('/calendar', methods=['GET'])
def calendar():
    month = request.args.get('month', date.today().month)
    year = request.args.get('year', date.today().year)
    locale = request.args.get('locale', current_app.config['LANGUAGES'])
    c = LocaleTextCalendar(locale=locale)
    current_app.logger.info('locale: '+str(locale))
    month_calendar = dict(
        year=int(year),
        month_number=int(month),
        month_name=c.formatmonthname(int(year), int(month), width=0).split()[0],
        week_days_name=[c.formatweekday(day, width=3).strip() for day in range(0, 7)],
        dates=[
            [dict(month=int(day.month), day=day.day, full_date=day.isoformat()) for day in week]
            for week in c.monthdatescalendar(int(year), int(month))
        ],
        _links=dict(next_month=url_for('api.calendar', _external=True, month=_nextmonth(int(year), int(month))),
                    prev_month=url_for('api.calendar', _external=True, month=_prevmonth(int(year), int(month))))
    )
    return jsonify(month_calendar)



@bp.route('/test', methods=['GET'])
@token_auth.login_required
def test():
    return jsonify({'key': 'value'})

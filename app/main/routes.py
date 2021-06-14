from flask import current_app, render_template, url_for, redirect
from app.main import bp
from calendar import Calendar, month_name, LocaleTextCalendar
from datetime import date
import requests
import json


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', name='anna')


@bp.route('/calendar', methods=['GET', 'POST'])
def calendar():
    r = requests.get(url_for('api.calendar', _external=True))
    month_calendar = json.loads(r.content.decode('utf-8-sig'))
    return render_template('month_calendar.html', name='anna', c=month_calendar)
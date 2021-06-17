from flask import current_app, render_template, url_for, redirect, g
from flask_login import current_user
from app.main import bp
from app.main.forms import CalendarForm, month_id
import requests
import json
from app.models import User


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first_or_404()
    else:
        user = None
    return render_template('index.html', user=user)


@bp.route('/calendar', methods=['GET', 'POST'])
def calendar():
    form = CalendarForm()
    if form.month.data and form.year.data:
        r = requests.get(url_for('api.calendar', _external=True),
                         params={'month': form.month.data, 'year': form.year.data})
        month_calendar = json.loads(r.content.decode('utf-8-sig'))
        return render_template('month_calendar.html', c=month_calendar, form=form)
    r = requests.get(url_for('api.calendar', _external=True))
    month_calendar = json.loads(r.content.decode('utf-8-sig'))
    return render_template('month_calendar.html', c=month_calendar, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    pass
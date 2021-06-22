from flask import current_app, render_template, url_for, redirect, request, jsonify, flash
from flask_login import current_user
from app.main import bp
from app.main.forms import CalendarForm, EventForm
import requests
import json
from app.models import User, Event
from datetime import date
from calendar import _nextmonth, _prevmonth


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

    # обявляем параметры запроса, если не заданы, то по умолчанию текущие год и месяц
    month = request.args.get('month', date.today().month)
    year = request.args.get('year', date.today().year)

    # при подтверждении формы (нажатие на кнопку "Показать") перенаправление на календарь с выбранными параметрами
    if form.validate_on_submit():
        return redirect(url_for('main.calendar', month=form.month.data, year=form.year.data))

    # получаем данные для отбражения календаря
    r = requests.get(url_for('api.calendar', _external=True),
                         params={'month': month, 'year': year})
    month_calendar = json.loads(r.content.decode('utf-8-sig'))
    # полчуаем данные для отображения событий
    r_events = requests.get(url_for('api.get_events', _external=True, id=current_user.id),
                            params={'month': month, 'year': year})
    events = json.loads(r_events.content.decode('utf-8-sig'))

    # задаем значения ссылок для навигации по месяцам и создания событий
    next_month = url_for('main.calendar', month=str(_nextmonth(int(year), int(month))[1]),
                                          year=str(_nextmonth(int(year), int(month))[0]))
    prev_month = url_for('main.calendar', month=str(_prevmonth(int(year), int(month))[1]),
                                          year=str(_prevmonth(int(year), int(month))[0]))
    curr_month = url_for('main.calendar')

    return render_template('month_calendar.html', c=month_calendar, form=form, today=date.today(), events=events,
                           next_month=next_month, curr_month=curr_month, prev_month=prev_month)


@bp.route('/add_event', methods=['GET', 'POST'])
def add_event(date_data=None):
    if date_data:
        pass   # будет записываться дата при инажатии на ячейку
    form = EventForm()
    if form.validate_on_submit():
        data = dict(date=dict(day=form.date.data.day,
                              month=form.date.data.month,
                              year=form.date.data.year),
                    summary=form.summary.data,
                    full_description=form.full_description.data)
        r_add_event = requests.post(url_for('api.add_event', _external=True, id=current_user.id), json=data)
        if r_add_event.status_code == 200:
            flash('Событие успешно добавлено')
        else:
            flash('Произошла ошибка')
        return redirect(url_for('main.calendar', month=form.date.data.month, year=form.date.data.year))
    return render_template('event_card.html', form=form)


@bp.route('/edit_event/<int:id>',  methods=['GET', 'POST'])
def edit_event(id):
    form = EventForm()
    event = current_user.events.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        data = dict(date=dict(day=form.date.data.day,
                              month=form.date.data.month,
                              year=form.date.data.year),
                    summary=form.summary.data,
                    full_description=form.full_description.data)
        r_edit_event = requests.put(url_for('api.edit_event', _external=True, id=event.id), json=data)
        if r_edit_event.status_code == 201:
            flash('Изменения успешно сохранены')
        else:
            flash('Произошла ошибка')
        return redirect(url_for('main.calendar', month=form.date.data.month, year=form.date.data.year))
    elif request.method == 'GET':
        form.date.data = event.date
        form.summary.data = event.summary
        form.full_description.data = event.full_description
    return render_template('event_card.html', form=form, event_id=event.id)


@bp.route('/delete_event/<int:id>', methods=['GET'])
def delete_event(id):
    event = current_user.events.filter_by(id=id).first_or_404()
    month, year = event.date.month, event.date.year
    r_delete_event = requests.delete(url_for('api.edit_event', _external=True, id=event.id))
    if r_delete_event.status_code == 204:
        flash('Событие успешно удалено')
    else:
        flash('Произошла ошибка')
    return redirect(url_for('main.calendar', month=month, year=year))


@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    pass
from flask import current_app, render_template, url_for, redirect, request, jsonify, flash
from flask_login import current_user, login_required
from app.main import bp
from app.main.forms import CalendarForm, EventForm, EmptyForm
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
        return redirect(url_for('main.calendar', month=form.month.data if form.month.data else None,
                                year=form.year.data if form.year.data else None))

    # получаем данные для отбражения календаря
    r = requests.get(url_for('api.calendar', _external=True),
                         params={'month': month, 'year': year})
    month_calendar = json.loads(r.content.decode('utf-8-sig'))
    # полчуаем данные для отображения событий
    if current_user.is_authenticated:
        r_events = requests.get(url_for('api.get_events', _external=True, id=current_user.id),
                                params={'month': month, 'year': year})
        events = json.loads(r_events.content.decode('utf-8-sig'))
    else:
        events = {}

    # задаем значения ссылок для навигации по месяцам и создания событий
    next_month = url_for('main.calendar', month=str(_nextmonth(int(year), int(month))[1]),
                                          year=str(_nextmonth(int(year), int(month))[0]))
    prev_month = url_for('main.calendar', month=str(_prevmonth(int(year), int(month))[1]),
                                          year=str(_prevmonth(int(year), int(month))[0]))
    curr_month = url_for('main.calendar')

    return render_template('month_calendar.html', c=month_calendar, form=form, today=date.today(), events=events,
                           next_month=next_month, curr_month=curr_month, prev_month=prev_month)


@bp.route('/add_event/', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    color_amount = len(form.color.choices)
    event_date = request.args.get('d')
    month, year = request.args.get('m', None), request.args.get('y', None)
    if event_date:
        form.date.data = date.fromisoformat(event_date)
    if form.validate_on_submit():
        data = dict(date=dict(day=form.date.data.day,
                              month=form.date.data.month,
                              year=form.date.data.year),
                    summary=form.summary.data,
                    full_description=form.full_description.data,
                    color=form.color.data if form.color.data else 'default')
        r_add_event = requests.post(url_for('api.add_event', _external=True, id=current_user.id), json=data)
        if r_add_event.status_code == 201:
            flash('Событие успешно добавлено')
        else:
            flash('Произошла ошибка')
        return redirect(url_for('main.calendar', month=form.date.data.month, year=form.date.data.year))
    return render_template('event_card.html', form=form, color_amount=color_amount, month=month, year=year)


@bp.route('/event/<int:id>',  methods=['GET', 'POST'])
@login_required
def event(id):
    form = EventForm()
    event = current_user.events.filter_by(id=id).first_or_404()
    color_amount = len(form.color.choices)
    form.validate()
    if form.validate_on_submit():
        data = dict(date=dict(day=form.date.data.day,
                              month=form.date.data.month,
                              year=form.date.data.year),
                    summary=form.summary.data,
                    full_description=form.full_description.data,
                    color=form.color.data if form.color.data else event.color,
                    done=form.done.data if form.done.data else False)
        r_edit_event = requests.put(url_for('api.edit_event', _external=True, id=event.id), json=data)
        print(r_edit_event.status_code)
        print(r_edit_event.content)
        if r_edit_event.status_code == 200:
            flash('Изменения успешно сохранены')
        elif r_edit_event.status_code == 201:
            flash('Событие создано')
        else:
            flash('Произошла ошибка')
        return redirect(url_for('main.calendar', month=form.date.data.month, year=form.date.data.year))
    elif request.method == 'GET':
        form.date.data = event.date
        form.summary.data = event.summary
        form.full_description.data = event.full_description
        form.color.data = event.color
        form.done.data = event.done
    return render_template('event_card.html', form=form, event=event, color_amount=color_amount)


@bp.route('/delete_event/<int:id>', methods=['GET'])
@login_required
def delete_event(id):
    event = current_user.events.filter_by(id=id).first_or_404()
    month, year = event.date.month, event.date.year
    r_delete_event = requests.delete(url_for('api.edit_event', _external=True, id=event.id))
    if r_delete_event.status_code == 204:
        flash('Событие успешно удалено')
    else:
        flash('Произошла ошибка')
    return redirect(url_for('main.calendar', month=month, year=year))


@bp.route('/event/<int:id>/popup')
@login_required
def user_popup(id):
    form=EmptyForm()
    event = Event.query.filter_by(id=id).first_or_404()
    return render_template('event_popup.html', event=event, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    pass


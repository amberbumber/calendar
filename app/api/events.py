from app.api import bp
from app import db
from app.models import User, Event
from flask import jsonify, request, current_app, url_for
from calendar import LocaleTextCalendar
from datetime import date
from app.api.errors import bad_request


@bp.route('/events/<int:id>', methods=['GET'])
def get_events(id):
    """GET получаение списка всех событий пользователя  по id пользователя за месяц + 1 неделя до и после"""
    month = request.args.get('month', date.today().month)
    year = request.args.get('year', date.today().year)
    user = User.query.get_or_404(id)
    if int(month) == 12:
        events = user.events.filter(
            Event.date >= date(int(year), int(month) - 1, 23), Event.date < date(int(year) + 1, 1, 7)).all()
    elif int(month) == 1:
        events = user.events.filter(
            Event.date >= date(int(year) - 1, 12, 23), Event.date < date(int(year), int(month) + 1, 7)).all()
    else:
        events = user.events.filter(
            Event.date >= date(int(year), int(month) - 1, 23), Event.date < date(int(year), int(month) + 1, 7)).all()
    events_dict = dict()
    # for day in range(1, calendar.monthrange(2021, 6)[1] + 1)
    # for event in events:
    #     if not events_dict.get(event.date.day):
    #         # если на такое число отсутствует ключ, создаем первое событие
    #         events_dict[event.date.day] = {}
    #         events_dict[event.date.day][0] = event.to_dict()
    #     else:
    #         # если на такое число уже есть события, создаем следующее за существующим
    #         events_dict[event.date.day][len(events_dict[event.date.day])] = event.to_dict()
    for i in range(len(events)):
        events_dict[i] = events[i].to_dict()

    return events_dict


@bp.route('/event/<int:id>', methods=['POST'])
def add_event(id):
    """POST - добавляет событие для пользователя по id пользователя"""
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'date' not in data or 'summary' not in data:
        return bad_request('must include date and summary')
    event = Event(user=user)
    event.from_dict(data)
    db.session.add(event)
    db.session.commit()
    response = jsonify(event.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_event', id=event.id)
    return response


@bp.route('/event/<int:id>', methods=['GET'])
def get_event(id):
    """GET - получить данные о событии по id события"""
    event = Event.query.get_or_404(id)
    return event.to_dict()


@bp.route('/event/<int:id>', methods=['PUT'])
def edit_event(id):
    """PUT - редактировать данные о событии по id события"""
    event = Event.query.get_or_404(id)
    data = request.get_json() or {}
    if 'date' not in data or 'summary' not in data:
        return bad_request('must include date and summary')
    event.from_dict(data)
    db.session.commit()
    return jsonify(event.to_dict())


@bp.route('/event/<int:id>', methods=['DELETE'])
def delete_event(id):
    """DELETE - удалить событие по id события"""
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    response = jsonify({})
    response.status_code = 204
    return response


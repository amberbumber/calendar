from flask import current_app, url_for
from app import db, login
import os
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime, timedelta, date


# загрузка зарегистрированного пользователя
# Пользовательский загрузчик зарегистрирован в Flask-Login с помощью декоратора @login.user_loader.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    events = db.relationship('Event', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
            'post_count': self.posts.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'followers': url_for('api.get_followers', id=self.id),
                'followed': url_for('api.get_followed', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(64))
    full_description = db.Column(db.String(128))
    date = db.Column(db.Date, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    color = db.Column(db.String(10))
    done = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return '<Event {}>'.format(self.summary)

    def to_dict(self):
        data = {
            'id': self.id,
            'summary': self.summary,
            'full_description': self.full_description,
            'date': self.date_to_dict(self.date),
            'color': self.color,
            'done': self.done
        }
        return data

    def from_dict(self, data):
        for field in ['summary', 'full_description', 'date', 'color', 'done']:
            if field in data:
                if field == 'date':
                    setattr(self, field, self.dict_to_date(data[field]))
                    continue
                if field == 'done' and type(data[field]) == str:
                    if data[field].lower() == 'false':
                        data[field] = False
                    else:
                        data[field] = True
                setattr(self, field, data[field])

    @staticmethod
    def dict_to_date(date_dict):
        return date(date_dict['year'], date_dict['month'], date_dict['day'])

    @staticmethod
    def date_to_dict(date_obj):
        return {'day': date_obj.day, 'month': date_obj.month, 'year': date_obj.year}
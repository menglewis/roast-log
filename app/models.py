import json
from datetime import datetime
from flask.ext.login import UserMixin
from app import db, bcrypt
from app.utils import convert_times_to_second_diff


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    beans = db.relationship('Bean', backref='user', lazy='dynamic')
    roasters = db.relationship('Roaster', backref='user', lazy='dynamic')
    roasts = db.relationship('Roast', backref='user', lazy='dynamic', order_by='desc(Roast.roast_datetime)')

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %s>' % self.username

    def roasts_by_bean(self):
        data = []
        for bean in self.beans.all():
            data.append({
                'label': bean.name,
                'value': len(bean.roasts.all()),
            })
        return json.dumps(data)

    def roast_weight_by_bean(self):
        data = []
        for bean in self.beans.all():
            data.append({
                'label': bean.name,
                'value': sum((roast.end_weight for roast in bean.roasts.all()))
            })
        return json.dumps(data)

    def roasts_by_roaster(self):
        data = []
        for roaster in self.roasters.all():
            data.append({
                'label': roaster.name,
                'value': len(roaster.roasts.all()),
            })
        return json.dumps(data)

    def roast_weight_by_roaster(self):
        data = []
        for roaster in self.roasters.all():
            data.append({
                'label': roaster.name,
                'value': sum((roast.end_weight for roast in roaster.roasts.all()))
            })
        return json.dumps(data)


class Bean(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    roasts = db.relationship('Roast', backref='bean', lazy='dynamic', order_by='desc(Roast.roast_datetime)')

    def roast_chart_data(self):
        data = []
        for roast in self.roasts.all():
            data.append({
                'x': roast.unix_datetime,
                'y': roast.end_weight,
                'label': roast.bean.name + " " + roast.roaster.name,
            })
        return json.dumps(data)

    def __repr__(self):
        return '<Bean %s>' % self.name


class Roaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    roasts = db.relationship('Roast', backref='roaster', lazy='dynamic', order_by='desc(Roast.roast_datetime)')

    def __repr__(self):
        return '<Roaster %s>' % self.name


class Roast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bean_id = db.Column(db.Integer, db.ForeignKey('bean.id'))
    roaster_id = db.Column(db.Integer, db.ForeignKey('roaster.id'))

    start_time = db.Column(db.String)
    start_temp = db.Column(db.Integer, nullable=True)
    start_weight = db.Column(db.Integer, nullable=True)

    fc_start_time = db.Column(db.String, nullable=True)
    fc_start_temp = db.Column(db.Integer, nullable=True)
    fc_end_time = db.Column(db.String, nullable=True)
    fc_end_temp = db.Column(db.Integer, nullable=True)

    sc_start_time = db.Column(db.String, nullable=True)
    sc_start_temp = db.Column(db.Integer, nullable=True)
    sc_end_time = db.Column(db.String, nullable=True)
    sc_end_temp = db.Column(db.Integer, nullable=True)

    end_time = db.Column(db.String)
    end_temp = db.Column(db.Integer, nullable=True)
    end_weight = db.Column(db.Integer, nullable=True)

    roast_datetime = db.Column(db.DateTime)
    notes = db.Column(db.Text, nullable=True)

    @property
    def time_elapsed(self):
        return convert_times_to_second_diff(self.start_time, self.end_time)

    @property
    def first_crack_start(self):
        return convert_times_to_second_diff(self.start_time, self.fc_start_time)

    @property
    def first_crack_end(self):
        return convert_times_to_second_diff(self.start_time, self.fc_end_time)

    @property
    def second_crack_start(self):
        return convert_times_to_second_diff(self.start_time, self.sc_start_time)

    @property
    def second_crack_end(self):
        return convert_times_to_second_diff(self.start_time, self.sc_end_time)

    @property
    def weight_loss(self):
        if self.start_weight and self.end_weight:
            return self.start_weight - self.end_weight

    @property
    def percent_weight_loss(self):
        if self.start_weight and self.end_weight:
            return round(float(self.weight_loss) / self.start_weight * 100, 2)
        return None

    @property
    def formatted_datetime(self):
        return self.roast_datetime.strftime("%m/%d/%Y %I:%M:%S %p")

    @property
    def unix_datetime(self):
        return (self.roast_datetime - datetime(1970, 1, 1)).total_seconds()

    def line_chart_data(self):
        data = []
        data.append({
            'x': 0,
            'y': self.start_temp,
            'label': 'Start',
        })
        if self.fc_start_time and self.fc_start_temp:
            data.append({
                'x': self.first_crack_start,
                'y': self.fc_start_temp,
                'label': 'First Crack Start',
            })
        if self.fc_end_time and self.fc_end_temp:
            data.append({
                'x': self.first_crack_end,
                'y': self.fc_end_temp,
                'label': 'First Crack End',
            })
        if self.sc_start_time and self.sc_start_temp:
            data.append({
                'x': self.second_crack_start,
                'y': self.sc_start_temp,
                'label': 'Second Crack Start',
            })
        if self.sc_end_time and self.sc_end_temp:
            data.append({
                'x': self.second_crack_end,
                'y': self.sc_end_temp,
                'label': 'Second Crack End',
            })
        data.append({
            'x': self.time_elapsed,
            'y': self.end_temp,
            'label': 'End',
        })
        return json.dumps(data)

    def __repr__(self):
        return '<Roast %s>' % self.id

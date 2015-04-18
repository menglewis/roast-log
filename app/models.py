from flask.ext.login import UserMixin
from app import db, bcrypt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String, nullable=False)

    beans = db.relationship('Bean', backref='user', lazy='dynamic')
    roasters = db.relationship('Roaster', backref='user', lazy='dynamic')
    roasts = db.relationship('Roast', backref='user', lazy='dynamic')

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


class Bean(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    roasts = db.relationship('Roast', backref='bean', lazy='dynamic')

    def __repr__(self):
        return '<Bean %s>' % self.name


class Roaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    roasts = db.relationship('Roast', backref='roaster', lazy='dynamic')

    def __repr__(self):
        return '<Roaster %s>' % self.name


class Roast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bean_id = db.Column(db.Integer, db.ForeignKey('bean.id'))
    roaster_id = db.Column(db.Integer, db.ForeignKey('roaster.id'))

    start_time = db.Column(db.Integer)
    start_temp = db.Column(db.Integer, nullable=True)
    start_weight = db.Column(db.Integer, nullable=True)

    first_crack_start_time = db.Column(db.Integer, nullable=True)
    first_crack_start_temp = db.Column(db.Integer, nullable=True)
    first_crack_end_time = db.Column(db.Integer, nullable=True)
    first_crack_end_temp = db.Column(db.Integer, nullable=True)

    second_crack_start_time = db.Column(db.Integer, nullable=True)
    second_crack_start_temp = db.Column(db.Integer, nullable=True)
    second_crack_end_time = db.Column(db.Integer, nullable=True)
    second_crack_end_temp = db.Column(db.Integer, nullable=True)

    end_time = db.Column(db.Integer)
    end_temp = db.Column(db.Integer, nullable=True)
    end_weight = db.Column(db.Integer, nullable=True)

    roast_datetime = db.Column(db.DateTime)
    notes = db.Column(db.Text, nullable=True)

    @property
    def time_elapsed(self):
        return self.end_time

    @property
    def first_crack_start(self):
        return self.first_crack_start_time

    @property
    def first_crack_end(self):
        return self.first_crack_end_time

    @property
    def second_crack_start(self):
        return self.second_crack_start_time

    @property
    def second_crack_end(self):
        return self.second_crack_end_time

    @property
    def percent_weight_loss(self):
        if self.start_weight and self.end_weight:
            return round(float(self.start_weight - self.end_weight) / self.start_weight * 100, 2)
        return None

    def __repr__(self):
        return '<Roast %s>' % self.id

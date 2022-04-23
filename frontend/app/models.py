from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    birth_year = db.Column(db.Integer)
    birth_place = db.Column(db.String(64))
    current_place = db.Column(db.String(64))
    favorite_band = db.Column(db.String(64))
    favorite_film = db.Column(db.String(64))
    feedback = db.relationship('Feedback', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(140))
    semantic = db.Column(db.String(20))
    info = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Feedback {}>'.format(self.feedback)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


from app import db

class User(db.Model):
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

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(140))
    semantic = db.Column(db.Integer)
    info = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Feedback {}>'.format(self.feedback)

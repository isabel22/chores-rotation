from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import datetime

db = SQLAlchemy()

class Team(db.Model):
	__tablename__ = 'teams'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    active = db.Column(db.Boolean, default=True)

class Chore(db.Model):
	__tablename__ = 'chores'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	required_users = db.Column(db.Integer, default=1)

class UserChore(db.Model):
	__tablename__ = 'user_chores'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	chore_id = db.Column(db.Integer, db.ForeignKey('chores.id'))
	active = db.Column(db.Boolean, default=False)
	last_turn = db.Column(db.DateTime, default=datetime.datetime.utcnow)

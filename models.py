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

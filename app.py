import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *
from slack import WebClient
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://isabel:@localhost/chores_rotation')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
client = WebClient(token=os.environ.get('SLACK_TOKEN'))

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()

@app.route('/current-turn', methods=['POST', 'GET'])
def current_turn():
    backend = current_user_for('backend')
    frontend = current_user_for('frontend')
    # pair = backend['name'] + ' - ' + frontend['name']
    return os.environ.get('DATABASE_URL')

@app.route('/next-turn', methods=['POST', 'GET'])
def next_turn():
    backend = next_user_for('backend')
    frontend = next_user_for('frontend')
    # pair = backend['name'] + ' - ' + frontend['name']
    # assign_new_topic_on_channels(pair)
    return "a"

@app.route('/new-team', methods=['POST'])
def new_team():
    name = request.args.get('name')
    if validate_unique_team(name) is True:
        return create_team(name)
    else:
        return "Team already exists"

@app.route('/new-user', methods=['POST'])
def new_user():
    email = request.args.get('email')
    name = request.args.get('name')
    team = request.args.get('team')

    if validate_unique_user(email) is True:
        return create_user(name, team, email)
    else:
        return "User already exists"

@app.route('/list-users', methods=['POST', 'GET'])
def list_users():
    try:
        users = User.query.all()
        return "\n".join(user.name + ' ' + str(user.team_id) for user in users)

    except Exception as e:
        return(str(e))

def next_user_for(team):
    current = current_user_for(team)
    next = find_user(team, current[team+'_id'] + 1)
    if next is None:
        next = find_user(team, 1)
    update(next, { '$set': { 'actual': True } })
    update(current, { '$set': { 'actual': False } })
    return next

def current_user_for(team):
    "a"
    # return mongo.db.admin_ops.find_one({'team': team, 'actual': True, 'enabled': True})

def update(user, values):
    ''
    # mongo.db.admin_ops.update_one(user, values)

def find_user(team, id):
    ''
    # return mongo.db.admin_ops.find_one({'team': team, team+'_id': id, 'enabled': True})

def assign_new_topic_on_channels(topic):
    channels = os.environ.get('CHANNELS').split(" ")
    for channel in channels:
        client.api_call(api_method='conversations.setTopic',json={ 'channel': channel,'topic': topic })

def validate_unique_team(name):
    try:
        team=Team.query.filter_by(name=name).first()
        if team is None:
            return True
        else:
            return False
    except Exception as e:
        return True

def create_team(name):
    try:
        team=Team(name=name)
        db.session.add(team)
        db.session.commit()
        return "Team added"
    except Exception as e:
        return(str(e))

def validate_unique_user(email):
    try:
        user=User.query.filter_by(email=email).first()
        if user is None:
            return True
        else:
            return False
    except Exception as e:
        return True

def create_user(name, team, email):
    try:
        team=Team.query.filter_by(name=team).first()
        user=User(name=name, email=email, team_id=team.id, active=True)
        db.session.add(user)
        db.session.commit()
        return "User added"
    except Exception as e:
        return(str(e))
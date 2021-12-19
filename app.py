import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *
from slack import WebClient
from flask import request
from datetime import datetime
from sqlalchemy import create_engine

app = Flask(__name__)
db_url = os.environ.get('DB_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
client = WebClient(token=os.environ.get('SLACK_TOKEN'))

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()

@app.route('/current-turn', methods=['POST', 'GET'])
def current_turn():
    chore = request.args.get('chore')
    current_user_ids = find_users_for(chore, "true")
    current_turn_names = value_for("name", current_user_ids)
    return ' - '.join(current_turn_names)

@app.route('/next-turn', methods=['POST', 'GET'])
def next_turn():
    chore = request.args.get('chore')
    return change_turn_for(chore)

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

@app.route('/new-chore', methods=['POST'])
def new_chore():
    name = request.args.get('name')
    required_users = request.args.get('required_users')

    if validate_unique_chore(name) is True:
        return create_chore(name, required_users)
    else:
        return "Chore already exists"

@app.route('/list-users', methods=['POST', 'GET'])
def list_users():
    try:
        users = User.query.all()
        return "\n".join(user.name + ' ' + str(user.team_id) for user in users)

    except Exception as e:
        return(str(e))

@app.route('/list-teams', methods=['POST', 'GET'])
def list_teams():
    try:
        teams = Team.query.all()
        return "\n".join(team.name for team in teams)

    except Exception as e:
        return(str(e))

@app.route('/list-chores', methods=['POST', 'GET'])
def list_chores():
    try:
        chores = Chore.query.all()
        return "\n".join(chore.name for chore in chores)

    except Exception as e:
        return(str(e))

@app.route('/assign-chore', methods=['POST', 'GET'])
def assign_chore():
    chore = request.args.get('chore')
    email = request.args.get('email')

    return assign(email, chore)

def assign(email, chore):
    try:
        user = User.query.filter_by(email=email).first()
        chore_object = Chore.query.filter_by(name=chore).first()
        if user is None or chore_object is None:
            return "Email or Chore does not exist"
        else:
            try:
                user_chore = UserChore.query.filter_by(user_id=user.id, chore_id=chore_object.id).first()

                if user_chore is None:
                    user_chore=UserChore(user_id=user.id, chore_id=chore_object.id, active=False, last_turn=datetime.now())
                    db.session.add(user_chore)
                    db.session.commit()
                    return user.name + " assigned to " + chore
                else:
                    return "Chore was already assigned to " + user.name

            except Exception as e:
                try:
                    user_chore=UserChore(user_id=user.id, chore_id=chore_object.id, active=False, last_turn=datetime.now())
                    db.session.add(user_chore)
                    db.session.commit()
                    return user.name + " assigned to " + chore
                except Exception as e:
                    return(str(e))

    except Exception as e:
        return (str(e))


def change_turn_for(chore):
    next_user_ids = find_users_for(chore, "false")
    current_user_ids = find_users_for(chore, "true")
    next_turn_names = value_for("name", next_user_ids)
    current_turn_names = value_for("name", current_user_ids)

    update_status_for(current_user_ids, False)
    update_status_for(next_user_ids, True)

    return " - ".join(next_turn_names)

def update_status_for(user_ids, status):
    mappings = []

    for user_chore in db.session.query(UserChore).filter(UserChore.user_id.in_(list(user_ids))).all():
        info = { 'id': user_chore.id, 'active': status }
        extra = { 'last_turn': datetime.now() }
        info = {**info, **extra} if status == True else info

        mappings.append(info)

    db.session.bulk_update_mappings(UserChore, mappings)
    db.session.flush()
    db.session.commit()

def find_users_for(chore, active_user):
    chore_id=Chore.query.filter_by(name=chore).first().id

    engine = create_engine(db_url)
    connection = engine.connect()
    result = connection.execute("select distinct on (team_id) team_id, u.id, name, email, last_turn from user_chores as uc, users as u where uc.active = " + active_user + " and uc.user_id = u.id and u.active = true and uc.chore_id = " + str(chore_id) + " order by team_id, last_turn asc")

    ids = []
    for row in result:
      ids.append(row['id'])

    return ids

def value_for(column, user_ids):
    engine = create_engine(db_url)
    connection = engine.connect()
    user_ids_str = ", ".join(str(value) for value in user_ids)
    result = connection.execute("select " + column + " from users where id in (" + user_ids_str + ")")
    names = []
    for row in result:
      names.append(row[0])

    return names

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

def validate_unique_chore(name):
    try:
        chore=Chore.query.filter_by(name=name).first()
        if chore is None:
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

def create_chore(name, required_users):
    try:
        chore=Chore(name=name, required_users=required_users)
        db.session.add(chore)
        db.session.commit()
        return "Chore added"
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
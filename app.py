import os
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

@app.route('/current-turn', methods=['POST', 'GET'])
def current_turn():
    backend = current_user_for('backend')
    frontend = current_user_for('frontend')
    pair = backend['name'] + ' - ' + frontend['name']
    return pair

@app.route('/next-turn', methods=['POST', 'GET'])
def next_turn():
    backend = next_user_for('backend')
    frontend = next_user_for('frontend')
    pair = backend['name'] + ' - ' + frontend['name']
    return pair

def next_user_for(team):
    current = current_user_for(team)
    next = find_user(team, current[team+'_id'] + 1)
    if next is None:
        next = find_user(team, 1)
    update(next, { '$set': { 'actual': True } })
    update(current, { '$set': { 'actual': False } })
    print(next)
    return next

def current_user_for(team):
    return mongo.db.admin_ops.find_one({'team': team, 'actual': True, 'enabled': True})

def update(user, values):
    mongo.db.admin_ops.update_one(user, values)

def find_user(team, id):
    return mongo.db.admin_ops.find_one({'team': team, team+'_id': id, 'enabled': True})

import flask
import mongoengine
from flask import Flask, make_response, request
from flask_pymongo import PyMongo


import json
from bson.objectid import ObjectId

app = Flask(__name__)


app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost/hospitols'
}
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/hospitols")
db = mongodb_client.db



def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__



@app.route("/hospital/<state>")
def get_Hospital_input(state):
    state_req = request.args.get('state')
    hospitals = db.hosp_info.find({"state": state})
    return json.dumps([hospital for hospital in hospitals], default=newEncoder )

@app.route("/hospital")
def get_Hospital_req():
    state_req = request.args.get('state')
    hospitals = db.hosp_info.find({"state": state_req})
    return json.dumps([hospital for hospital in hospitals], default=newEncoder )


@app.route("/add_one_note")
def add_one():
    db.todos.insert_one({'provider_id': "000003", 'body': "todo two"})
    return flask.jsonify(message="success")

@app.route("/add_one_hospital")
def add_one_hospital():
    db.hosp_info.insert_one({'provider_id': "000003", 'body': "todo two"})
    return flask.jsonify(message="success")




if __name__ == '__main__':
    app.run()


